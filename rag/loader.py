from typing import List, Union, Tuple, Optional
from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader, CSVLoader, Docx2txtLoader, JSONLoader,
    UnstructuredHTMLLoader, UnstructuredPDFLoader, PyPDFLoader
)
import logging
import pytesseract
from pdf2image import convert_from_path
import os
import platform
from dotenv import load_dotenv
import fitz  # PyMuPDF
import pandas as pd
import pdfplumber
from enum import Enum
import nltk
import re

# NLTK 리소스 다운로드
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('averaged_perceptron_tagger')  # 추가로 필요한 리소스

logger = logging.getLogger(__name__)

class DocumentLoaderType(Enum):
    PYPDF = "pypdf"
    UNSTRUCTURED = "unstructured"
    FITZ = "fitz"
    PDFPLUMBER = "pdfplumber"
    TESSARACT = "tesseract"
    TEXT = "text"
    CSV = "csv"
    DOCX = "docx"
    JSON = "json"
    HTML = "html"
    EXCEL = "excel"

class DocumentLoader:
    def __init__(self, file_name: str, pdf_loader_type: Optional[str] = None):
        # .env 파일 로드
        load_dotenv()
        
        self.loaders = {
            '.pdf': (self._load_pdf_with_ocr, pdf_loader_type),  # 튜플로 변경
            '.txt': (TextLoader, DocumentLoaderType.TEXT),
            '.csv': (CSVLoader, DocumentLoaderType.CSV),
            '.docx': (Docx2txtLoader, DocumentLoaderType.DOCX),
            '.json': (JSONLoader, DocumentLoaderType.JSON),
            '.html': (UnstructuredHTMLLoader, DocumentLoaderType.HTML),
            '.xlsx': (self._load_excel, DocumentLoaderType.EXCEL)
        }
        
        # 파일 확장자에 따른 로더 타입 설정
        file_extension = Path(file_name).suffix.lower()
        if file_extension not in self.loaders:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {file_extension}")
            
        if file_extension == '.pdf':
            # PDF 파일인 경우 로더 타입 설정
            logger.info(f"PDF 로더 타입 파라미터: {pdf_loader_type}")
            if pdf_loader_type:
                try:
                    self.loader_type = DocumentLoaderType(pdf_loader_type)
                    logger.info(f"PDF 로더 타입 설정됨: {self.loader_type.value}")
                except ValueError as e:
                    logger.warning(f"잘못된 PDF 로더 타입: {pdf_loader_type}, 기본값(PYPDF)으로 설정됩니다. 오류: {str(e)}")
                    self.loader_type = DocumentLoaderType.PYPDF
            else:
                logger.info("PDF 로더 타입이 지정되지 않았습니다. 기본값(PYPDF)으로 설정됩니다.")
                self.loader_type = DocumentLoaderType.PYPDF
        else:
            # PDF가 아닌 경우 미리 정의된 로더 타입 사용
            _, self.loader_type = self.loaders[file_extension]
            logger.info(f"PDF가 아닌 파일의 로더 타입 설정: {self.loader_type.value}")
        
        # 운영체제별 Poppler 경로 설정
        if platform.system() == 'Windows':
            poppler_path = os.getenv('POPPLER_PATH_WINDOWS')
            tesseract_path = os.getenv('TESSERACT_PATH_WINDOWS')
        else:
            poppler_path = os.getenv('POPPLER_PATH_LINUX')
            tesseract_path = os.getenv('TESSERACT_PATH_LINUX')
            
        if poppler_path and os.path.exists(poppler_path):
            self.poppler_path = poppler_path
            logger.info(f"Poppler 경로 설정: {poppler_path}")
        else:
            logger.warning(f"Poppler 경로를 찾을 수 없습니다: {poppler_path}")
            self.poppler_path = None
            
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            logger.info(f"Tesseract 경로 설정: {tesseract_path}")
        else:
            logger.warning(f"Tesseract 경로를 찾을 수 없습니다: {tesseract_path}")

    def _load_excel(self, file_path: str) -> List[str]:
        """Excel 파일을 로드하고 텍스트로 변환합니다."""
        try:
            # Excel 파일 읽기
            df = pd.read_excel(file_path)
            
            # 각 행을 구조화된 텍스트로 변환
            texts = []
            for _, row in df.iterrows():
                # 각 열의 값을 텍스트로 변환
                row_text = []
                for column in df.columns:
                    value = str(row[column]) if pd.notna(row[column]) else ""
                    row_text.append(f"{column}: {value}")
                
                # 행의 모든 열 값을 하나의 텍스트로 결합
                text = ", ".join(row_text)
                texts.append(text)
            
            return texts
            
        except Exception as e:
            logger.error(f"Excel 파일 로드 중 오류 발생: {str(e)}")
            raise

    def _load_pdf_with_loader(self, file_path: str) -> List[str]:
        """선택된 PDF 로더를 사용하여 PDF를 로드합니다."""
        try:
            if self.loader_type == DocumentLoaderType.PYPDF:
                loader = PyPDFLoader(file_path, extract_images=False)
                documents = loader.load()
                texts = []
                for doc in documents:
                    # 텍스트 정규화
                    text = doc.page_content
                    if text.strip():
                        texts.append(text)
                return texts
            elif self.loader_type == DocumentLoaderType.UNSTRUCTURED:
                loader = UnstructuredPDFLoader(file_path, mode="elements",strategy="fast", chunking_strategy="by_title", include_orig_elements=False, multipage_sections=False, max_characters=4000, overlap=200)
                documents = loader.load()
                texts = []
                for doc in documents:
                    if isinstance(doc.page_content, str):
                        # 중복 문자 제거 정규식
                        text = re.sub(r'([가-힣])\1+', r'\1', doc.page_content)
                        # CID 문자열을 제거
                        text = re.sub(r'\(cid:\d+\)', '', text)
                        if text.strip():  # 빈 문자열이 아닌 경우만 추가
                            texts.append(text)
                    elif isinstance(doc.page_content, dict):
                        text = str(doc.page_content.get('text', ''))
                        # 중복 문자 제거 정규식
                        text = re.sub(r'([가-힣])\1+', r'\1', text)
                        text = re.sub(r'\(cid:\d+\)', '', text)
                        if text.strip():
                            texts.append(text)
                    else:
                        text = str(doc.page_content)
                        # 중복 문자 제거 정규식
                        text = re.sub(r'([가-힣])\1+', r'\1', text)
                        text = re.sub(r'\(cid:\d+\)', '', text)
                        if text.strip():
                            texts.append(text)
                return texts
            elif self.loader_type == DocumentLoaderType.FITZ:
                doc = fitz.open(file_path)
                texts = []
                for page in doc:
                    text = page.get_text()
                    if text.strip():
                        texts.append(text)
                return texts
            elif self.loader_type == DocumentLoaderType.PDFPLUMBER:
                texts = []
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        try:
                            text = page.extract_text()
                            text = re.sub(r'([가-힣])\1+', r'\1', text)
                            text = re.sub(r'\(cid:\d+\)', '', text)
                            if text and text.strip():
                                texts.append(text)
                        except UnicodeDecodeError:
                            # 문제가 있는 페이지는 건너뛰기
                            continue
                return texts
        except Exception as e:
            logger.error(f"PDF 로드 중 오류 발생: {str(e)}")
            raise

    def _is_pdf_ocr_processed(self, file_path: str) -> bool:
        """PDF가 이미 OCR 처리되었는지 확인합니다."""
        try:
            doc = fitz.open(file_path)
            total_text = ""
            
            # 첫 페이지의 텍스트를 확인
            page = doc[0]
            text = page.get_text()
            total_text += text
            
            # 텍스트가 충분히 있는지 확인 (임계값: 10자)
            if len(total_text.strip()) > 10:
                logger.info("PDF에 텍스트 레이어가 존재합니다. OCR이 이미 처리된 것으로 판단됩니다.")
                return True
                
            # 이미지가 있는지 확인
            images = page.get_images()
            if images:
                logger.info("PDF에 이미지가 존재합니다. OCR이 필요한 것으로 판단됩니다.")
                return False
                
            logger.info("PDF의 상태를 명확히 판단할 수 없습니다.")
            return False
            
        except Exception as e:
            logger.error(f"PDF 상태 확인 중 오류 발생: {str(e)}")
            return False

    def _load_pdf_with_ocr(self, file_path: str) -> List[str]:
        """OCR을 사용하여 PDF에서 텍스트를 추출합니다."""
        try:
            # PDF의 OCR 상태 확인
            if self._is_pdf_ocr_processed(file_path):
                return self._load_pdf_with_loader(file_path)
            
            # OCR이 필요한 경우 이미지 변환 및 OCR 처리
            self.loader_type = DocumentLoaderType.TESSARACT
            if self.poppler_path:
                images = convert_from_path(file_path, poppler_path=self.poppler_path)
            else:
                images = convert_from_path(file_path)
            
            # 각 페이지에서 텍스트 추출
            texts = []
            for i, image in enumerate(images):
                # 이미지에서 텍스트 추출
                text = pytesseract.image_to_string(image, lang='kor+eng')
                if text.strip():  # 텍스트가 있는 경우만 추가
                    texts.append(text)
            
            # 텍스트가 없는 경우 선택된 PDF 로더로 시도
            if not texts:
                texts = self._load_pdf_with_loader(file_path)
            
            return texts
            
        except Exception as e:
            logger.error(f"PDF OCR 처리 중 오류 발생: {str(e)}")
            # OCR 실패 시 선택된 PDF 로더로 시도
            try:
                return self._load_pdf_with_loader(file_path)
            except Exception as e:
                logger.error(f"PDF 로드 중 오류 발생: {str(e)}")
                raise

    def load_document(self, file_path: Union[str, Path]) -> List[str]:
        """문서를 로드하고 텍스트로 변환합니다."""
        try:
            file_path = Path(file_path)
            file_extension = file_path.suffix.lower()
            
            if file_extension not in self.loaders:
                raise ValueError(f"지원하지 않는 파일 형식입니다: {file_extension}")
            
            loader_func, _ = self.loaders[file_extension]
            
            if file_extension == '.pdf':
                texts = loader_func(str(file_path))
            elif file_extension == '.xlsx':
                texts = loader_func(str(file_path))
            else:
                loader = loader_func(str(file_path))
                documents = loader.load()
                texts = [doc.page_content for doc in documents]
            
            return texts
            
        except Exception as e:
            logger.error(f"문서 로드 중 오류 발생: {str(e)}")
            raise
