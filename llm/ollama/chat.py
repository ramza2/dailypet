from typing import List, Optional, AsyncGenerator
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from repository.dog_docs_repository import DogDocsRepository
from repository.dog_chats_repository import DogChatsRepository
from repository.pet_repository import PetRepository
from repository.dog_meal_repository import DogMealRepository
from repository.dog_snack_repository import DogSnackRepository
from repository.dog_walk_repository import DogWalkRepository
from repository.dog_temperature_repository import DogTemperatureRepository
from repository.pulse_repository import PulseRepository
from repository.respiration_repository import RespirationRepository
from entity.dog_chat import DogChat
from entity.pet import Pet
from datetime import datetime, timedelta
from llm.model import get_model
import logging
from fastapi import HTTPException
import json
import os

logger = logging.getLogger(__name__)

# 전역 변수로 모델을 한 번만 로드
_model = get_model()

DEFAULT_OLLAMA_CHAT_MODEL = "gemma3"
DEFAULT_OLLAMA_TEMPERATURE = 0.6
DEFAULT_OLLAMA_TOP_P = 0.9
DEFAULT_OLLAMA_REPEAT_PENALTY = 1.1
DEFAULT_OLLAMA_NUM_CTX = 2048
MAX_SAFE_CPU_THREADS = 8


def _resolve_thread_count() -> int:
    """CPU 환경에서 과도한 스레드 사용을 방지하기 위해 스레드 수를 계산합니다."""
    env_value = os.getenv("OLLAMA_NUM_THREAD")
    if env_value:
        try:
            return max(1, int(env_value))
        except ValueError:
            logger.warning(f"OLLAMA_NUM_THREAD 값이 잘못되었습니다: {env_value}. 자동 계산값을 사용합니다.")

    cpu_count = os.cpu_count() or 1
    # 시스템 여유를 위해 1개 코어는 남기고, 과도한 컨텍스트 스위칭을 막기 위해 상한을 둡니다.
    return max(1, min(MAX_SAFE_CPU_THREADS, cpu_count - 1))

class DogChatSystem:
    def __init__(
        self, 
        docs_repo: DogDocsRepository, 
        chats_repo: DogChatsRepository, 
        profile_repo: PetRepository,
        dog_meal_repo: DogMealRepository,
        dog_snack_repo: DogSnackRepository,
        dog_walk_repo: DogWalkRepository,
        dog_temperature_repo: DogTemperatureRepository,
        pulse_repo: PulseRepository,
        respiration_repo: RespirationRepository
    ):
        model_name = os.getenv("OLLAMA_CHAT_MODEL", DEFAULT_OLLAMA_CHAT_MODEL)
        num_ctx = int(os.getenv("OLLAMA_NUM_CTX", str(DEFAULT_OLLAMA_NUM_CTX)))
        temperature = float(os.getenv("OLLAMA_TEMPERATURE", str(DEFAULT_OLLAMA_TEMPERATURE)))
        top_p = float(os.getenv("OLLAMA_TOP_P", str(DEFAULT_OLLAMA_TOP_P)))
        repeat_penalty = float(os.getenv("OLLAMA_REPEAT_PENALTY", str(DEFAULT_OLLAMA_REPEAT_PENALTY)))
        num_thread = _resolve_thread_count()
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")

        self.llm = Ollama(
            model=model_name,
            base_url=ollama_base_url,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
            num_ctx=num_ctx,
            num_thread=num_thread,
        )
        logger.info(
            f"Ollama 설정 - base_url={ollama_base_url}, model={model_name}, num_ctx={num_ctx}, "
            f"num_thread={num_thread}, temperature={temperature}, top_p={top_p}, "
            f"repeat_penalty={repeat_penalty}"
        )
        self.embeddings = _model
        self.docs_repo = docs_repo
        self.chats_repo = chats_repo
        self.profile_repo = profile_repo
        self.dog_meal_repo = dog_meal_repo
        self.dog_snack_repo = dog_snack_repo
        self.dog_walk_repo = dog_walk_repo
        self.dog_temperature_repo = dog_temperature_repo
        self.pulse_repo = pulse_repo
        self.respiration_repo = respiration_repo
        self.llm_provider = "ollama"
        
        # 프롬프트 템플릿 설정
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question", "chat_history", "dog_profile"],
            template_format="jinja2",
            template = """
너는 반려견 건강 전문가이자 수의사입니다.

- 사용자의 질문에 대해 항상 **자연스러운 한국어 문장**으로 답변해주세요.
- 응답은  **친근하고 상담하는 듯한 구어체**로 작성해 주세요.
- 답변내용에서 "일반적으로" 또는 "수의사와 상담해서" 와 같은 모호한 내용은 제외해줘
- 답변내용은 명확하고 직접적인 수치기반으로 핵심내용만 정리해서 알려줘.
- 외래어 사용이 필요한 경우에는 괄호를 사용하여 한글 설명을 함께 제공해 주세요. 예: 스트레스(stress)
- "질문:", "답변:", "키워드:" 등의 메타 문구는 포함하지 마세요.

---

반려견 정보:
{{ dog_profile }}

{% if context and context.strip() %}
참고 문서 (한글로 작성됨):
{{ context }}
{% endif %}

{% if chat_history and chat_history.strip() %}
이전 대화 내용:
{{ chat_history }}
{% endif %}

사용자의 질문:
{{ question }}

응답:
"""
        )
        
        # LLMChain을 RunnableSequence로 변경
        self.chain = self.prompt_template | self.llm
        
    async def _get_relevant_docs(self, query: str, k: int = 3) -> List[str]:
        """질문과 관련된 문서를 검색합니다."""
        # 질문의 임베딩 생성
        query_embedding = self.embeddings.encode(query, normalize_embeddings=True)
        
        # 데이터베이스에서 유사한 문서 검색
        similar_docs = await self.docs_repo.search_similar_docs(query_embedding, k)
        return [doc.content for doc in similar_docs]
        
    def _format_chat_history(self, chat_history: List[DogChat]) -> str:
        """채팅 기록을 문자열로 포맷팅합니다."""
        if not chat_history:
            return ""
            
        # 시간 순으로 정렬
        sorted_history = sorted(chat_history, key=lambda x: x.created_at)
        
        formatted_history = []
        for chat in sorted_history:
            formatted_history.append(f"사용자: {chat.message}")
            formatted_history.append(f"AI: {chat.response}")
            
        return "\n".join(formatted_history)

    async def _get_health_monitoring_data(self, dog_id: int) -> str:
        """최근 한달간의 건강 모니터링 데이터를 조회합니다."""
        try:
            # 한달 전 날짜 계산
            one_month_ago = datetime.now() - timedelta(days=30)
            
            # 각 Repository에서 데이터 조회
            meals = await self.dog_meal_repo.get_by_pet_id_and_date(dog_id, one_month_ago)
            snacks = await self.dog_snack_repo.get_by_pet_id_and_date(dog_id, one_month_ago)
            walks = await self.dog_walk_repo.get_by_pet_id_and_date(dog_id, one_month_ago)
            respiratory_rates = await self.respiration_repo.get_by_pet_id_and_date(dog_id, one_month_ago)
            heart_rates = await self.pulse_repo.get_by_pet_id_and_date(dog_id, one_month_ago)
            temperatures = await self.dog_temperature_repo.get_by_pet_id_and_date(dog_id, one_month_ago)
            
            # 데이터 요약 구성
            summary_parts = []
            summary_parts.append("최근 한달간의 건강 모니터링 데이터:")
            
            # 1. 식사 기록 (데이터가 있을 때만)
            if meals:
                summary_parts.append(f"""
            1. 식사 기록:
            - 총 식사 횟수: {len(meals)}회
            - 식사 타입 분포: {self._count_types([meal.meal_type for meal in meals])}
            - 평균 식사량: {sum(meal.amount for meal in meals) / len(meals):.1f}g (하루 평균: {sum(meal.amount for meal in meals) / 30:.1f}g)""")

            # 2. 간식 기록 (데이터가 있을 때만)
            if snacks:
                summary_parts.append(f"""
            2. 간식 기록:
            - 총 간식 횟수: {len(snacks)}회
            - 간식 타입 분포: {self._count_types([snack.snack_type for snack in snacks])}
            - 평균 간식량: {sum(snack.amount for snack in snacks) / len(snacks):.1f}개""")

            # 3. 산책 기록 (데이터가 있을 때만)
            if walks:
                summary_parts.append(f"""
            3. 산책 기록:
            - 총 산책 횟수: {len(walks)}회
            - 평균 산책 시간: {sum(walk.duration for walk in walks) / len(walks):.1f}분
            - 평균 산책 거리: {sum(walk.distance for walk in walks) / len(walks):.2f}km
            - 특이 행동 발생: {self._count_types([walk.activity_level for walk in walks if walk.activity_level])}""")

            # 4. 호흡수 측정 (데이터가 있을 때만)
            if respiratory_rates:
                summary_parts.append(f"""
            4. 호흡수 측정:
            - 총 측정 횟수: {len(respiratory_rates)}회
            - 평균 호흡수: {sum(rate['rate'] for rate in respiratory_rates) / len(respiratory_rates):.1f}회/분
            - 최소/최대: {min(rate['rate'] for rate in respiratory_rates)}/{max(rate['rate'] for rate in respiratory_rates)}회/분""")

            # 5. 심박수 측정 (데이터가 있을 때만)
            if heart_rates:
                summary_parts.append(f"""
            5. 심박수 측정:
            - 총 측정 횟수: {len(heart_rates)}회
            - 평균 심박수: {sum(rate['rate'] for rate in heart_rates) / len(heart_rates):.1f}bpm
            - 최소/최대: {min(rate['rate'] for rate in heart_rates)}/{max(rate['rate'] for rate in heart_rates)}bpm""")

            # 6. 체온 측정 (데이터가 있을 때만)
            if temperatures:
                summary_parts.append(f"""
            6. 체온 측정:
            - 총 측정 횟수: {len(temperatures)}회
            - 평균 체온: {sum(temp.temperature for temp in temperatures) / len(temperatures):.1f}°C
            - 최소/최대: {min(temp.temperature for temp in temperatures):.1f}/{max(temp.temperature for temp in temperatures):.1f}°C""")

            # 데이터가 하나도 없는 경우
            if not any([meals, snacks, walks, respiratory_rates, heart_rates, temperatures]):
                return "최근 한달간의 건강 모니터링 데이터가 없습니다."
            
            return "\n".join(summary_parts)
        except Exception as e:
            logger.error(f"건강 모니터링 데이터 조회 중 오류 발생: {str(e)}")
            return "건강 모니터링 데이터를 조회할 수 없습니다."

    def _count_types(self, items: List[str]) -> str:
        """리스트에서 각 항목의 출현 횟수를 집계합니다."""
        from collections import Counter
        counter = Counter(items)
        return ", ".join([f"{k}: {v}회" for k, v in counter.items()])

    def _build_prompt(self, message: str, context: str = "", chat_history: str = "", dog_profile_prompt: str = "") -> str:
        """프롬프트를 구성합니다."""
        # Jinja2 템플릿 변수를 올바르게 치환
        prompt = self.prompt_template.template
        
        # context가 빈 문자열이면 해당 섹션 제거
        if not context or not context.strip():
            prompt = prompt.replace("참고 문서 (한글로 작성됨):\n{{ context }}\n\n", "")
        else:
            prompt = prompt.replace("{{ context }}", context)
            
        # chat_history가 빈 문자열이면 해당 섹션 제거
        if not chat_history or not chat_history.strip():
            prompt = prompt.replace("이전 대화 내용:\n{{ chat_history }}\n\n", "")
        else:
            prompt = prompt.replace("{{ chat_history }}", chat_history)
            
        # 사용자 질문 추가
        prompt = prompt.replace("{{ question }}", message)
        
        # 반려견 프로필 프롬프트 추가
        prompt = prompt.replace("{{ dog_profile }}", dog_profile_prompt)
        
        return prompt.strip()

    async def chat_with_dog(self, dog_id: int, message: str) -> str:
        try:
            logger.info(f"채팅 요청 수신: dog_id={dog_id}, message={message}")
            
            # 반려견 프로필 조회
            dog_profile = await self.profile_repo.get_pet(dog_id)
            
            if not dog_profile:
                raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")
            
            logger.info(f"반려견 프로필 조회 완료: {dog_profile.name}")

            # 관련 문서 검색
            relevant_docs = await self._get_relevant_docs(message, 10)
            context = "\n".join(relevant_docs) if relevant_docs else ""
            
            # 건강 모니터링 데이터 조회
            health_monitoring_data = await self._get_health_monitoring_data(dog_id)
            
            # 시스템 프롬프트 생성
            size_map = {"L": "대형", "M": "중형", "S": "소형"}
            size_type = size_map.get(dog_profile.classification, "알수없음")
            dog_profile_prompt = f"""
            이름: {dog_profile.name}
            품종: {dog_profile.breed}
            성별: {dog_profile.gender}
            중성화 여부: {'완료' if dog_profile.neutering_yn == 'Y' else '미완료'}
            생년월일: {dog_profile.birthday}
            입양일: {dog_profile.adoption_date}
            체중: {dog_profile.weight}kg
            크기 분류: {size_type}
            BCS 유형: {dog_profile.bcs_type}
            건강 상태: {dog_profile.health_status}
            건강 이슈: {dog_profile.health_issues if dog_profile.health_issues else '없음'}
            최근 진단일: {dog_profile.last_checkup_date}

            {health_monitoring_data}
            """
            
            # 이전 대화 이력 조회
            pet = await self.profile_repo.get_pet(dog_id)
            if not pet:
                raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")
                
            chat_history = await self.chats_repo.get_recent_chats_by_uid(pet.uid, llm_provider=self.llm_provider)
            formatted_history = self._format_chat_history(chat_history)
            
            # 응답 생성
            result = self.chain.invoke({
                "context": context,
                "question": message,
                "chat_history": formatted_history,
                "dog_profile": dog_profile_prompt
            })

            # 응답 텍스트 추출
            response = result.get('text', '') if isinstance(result, dict) else str(result)
            
            # 메시지 임베딩 생성
            message_embedding = self.embeddings.encode(message, normalize_embeddings=True)
            
            # 채팅 이력 저장
            pet = await self.profile_repo.get_pet(dog_id)
            if not pet:
                raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")

            chat = DogChat(
                message=message,
                response=response,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                dog_id=dog_id,
                uid=pet.uid,
                message_embedding=message_embedding,
                llm_provider="ollama",
                prompt_template_text=self.prompt_template.template if hasattr(self, 'prompt_template') and hasattr(self.prompt_template, 'template') else None
            )
            await self.chats_repo.create_chat(chat)
            
            return response
        except Exception as e:
            logger.error(f"채팅 처리 중 오류 발생: {str(e)}")
            raise HTTPException(status_code=500, detail="채팅 처리 중 오류가 발생했습니다.")

    async def chat_with_dog_stream(self, dog_id: int, message: str) -> AsyncGenerator[str, None]:
        """스트리밍 방식으로 채팅 응답을 생성합니다."""
        try:
            logger.info(f"스트리밍 채팅 요청 수신: dog_id={dog_id}, message={message}")
            
            # 반려견 프로필 조회
            dog_profile = await self.profile_repo.get_pet(dog_id)
            
            if not dog_profile:
                raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")
            
            logger.info(f"반려견 프로필 조회 완료: {dog_profile.name}")

            # 관련 문서 검색
            relevant_docs = await self._get_relevant_docs(message, 10)
            context = "\n".join(relevant_docs) if relevant_docs else ""
            
            # 건강 모니터링 데이터 조회
            health_monitoring_data = await self._get_health_monitoring_data(dog_id)
            
            # 시스템 프롬프트 생성
            size_map = {"L": "대형", "M": "중형", "S": "소형"}
            size_type = size_map.get(dog_profile.classification, "알수없음")
            dog_profile_prompt = f"""
            이름: {dog_profile.name}
            품종: {dog_profile.breed}
            성별: {dog_profile.gender}
            중성화 여부: {'완료' if dog_profile.neutering_yn == 'Y' else '미완료'}
            생년월일: {dog_profile.birthday}
            입양일: {dog_profile.adoption_date}
            체중: {dog_profile.weight}kg
            크기 분류: {size_type}
            BCS 유형: {dog_profile.bcs_type}
            건강 상태: {dog_profile.health_status}
            건강 이슈: {dog_profile.health_issues if dog_profile.health_issues else '없음'}
            최근 진단일: {dog_profile.last_checkup_date}

            {health_monitoring_data}
            """
            
            # 이전 대화 이력 조회
            pet = await self.profile_repo.get_pet(dog_id)
            if not pet:
                raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")
                
            chat_history = await self.chats_repo.get_recent_chats_by_uid(pet.uid, llm_provider=self.llm_provider)
            formatted_history = self._format_chat_history(chat_history)
            
            # 프롬프트 구성
            prompt = self._build_prompt(message, context, formatted_history, dog_profile_prompt)
            
            logger.info(f"프롬프트 구성 완료, 길이: {len(prompt)}")
            
            # 스트리밍 응답 생성
            full_response = ""
            
            # LangChain chain을 사용한 스트리밍
            try:
                logger.info("LangChain 스트리밍 시작")
                
                # chain에 입력 데이터 준비
                input_data = {
                    "context": context,
                    "question": message,
                    "chat_history": formatted_history,
                    "dog_profile": dog_profile_prompt
                }
                
                # 스트리밍 실행
                async for chunk in self.chain.astream(input_data):
                    if hasattr(chunk, 'content') and chunk.content:
                        chunk_text = chunk.content
                        full_response += chunk_text
                        # SSE 형식으로 데이터 전송
                        yield f"data: {json.dumps({'content': chunk_text, 'done': False})}\n\n"
                    elif isinstance(chunk, str) and chunk.strip():
                        chunk_text = chunk.strip()
                        full_response += chunk_text
                        # SSE 형식으로 데이터 전송
                        yield f"data: {json.dumps({'content': chunk_text, 'done': False})}\n\n"
                
                logger.info("LangChain 스트리밍 완료")
                
            except Exception as e:
                logger.error(f"LangChain 스트리밍 중 오류: {str(e)}")
                raise
            
            # 메시지 임베딩 생성
            message_embedding = self.embeddings.encode(message, normalize_embeddings=True)
            
            # 채팅 이력 저장
            chat = DogChat(
                message=message,
                response=full_response,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                dog_id=dog_id,
                uid=pet.uid,
                message_embedding=message_embedding,
                llm_provider="ollama",
                prompt_template_text=self.prompt_template.template if hasattr(self, 'prompt_template') and hasattr(self.prompt_template, 'template') else None
            )
            await self.chats_repo.create_chat(chat)
            
            logger.info("채팅 이력 저장 완료")
            
            # 스트리밍 완료 신호
            yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
            
        except Exception as e:
            logger.error(f"스트리밍 채팅 처리 중 오류 발생: {str(e)}")
            error_data = json.dumps({'error': str(e), 'done': True})
            yield f"data: {error_data}\n\n"

    async def chat_with_prompt_template_stream(self, dog_id: int, message: str, template_content: str) -> AsyncGenerator[str, None]:
        """프롬프트 템플릿을 사용하여 스트리밍 방식으로 채팅 응답을 생성합니다."""
        try:
            logger.info(f"프롬프트 템플릿 스트리밍 채팅 요청 수신: dog_id={dog_id}, message={message}")
            
            # 반려견 프로필 조회
            dog_profile = await self.profile_repo.get_pet(dog_id)
            
            if not dog_profile:
                raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")
            
            logger.info(f"반려견 프로필 조회 완료: {dog_profile.name}")

            # 관련 문서 검색
            relevant_docs = await self._get_relevant_docs(message, 10)
            context = "\n".join(relevant_docs) if relevant_docs else ""
            
            # 건강 모니터링 데이터 조회
            health_monitoring_data = await self._get_health_monitoring_data(dog_id)
            
            # 시스템 프롬프트 생성
            size_map = {"L": "대형", "M": "중형", "S": "소형"}
            size_type = size_map.get(dog_profile.classification, "알수없음")
            dog_profile_prompt = f"""
            이름: {dog_profile.name}
            품종: {dog_profile.breed}
            성별: {dog_profile.gender}
            중성화 여부: {'완료' if dog_profile.neutering_yn == 'Y' else '미완료'}
            생년월일: {dog_profile.birthday}
            입양일: {dog_profile.adoption_date}
            체중: {dog_profile.weight}kg
            크기 분류: {size_type}
            BCS 유형: {dog_profile.bcs_type}
            건강 상태: {dog_profile.health_status}
            건강 이슈: {dog_profile.health_issues if dog_profile.health_issues else '없음'}
            최근 진단일: {dog_profile.last_checkup_date}

            {health_monitoring_data}
            """
            
            # 이전 대화 이력 조회
            pet = await self.profile_repo.get_pet(dog_id)
            if not pet:
                raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")
                
            chat_history = await self.chats_repo.get_recent_chats_by_uid(pet.uid, llm_provider=self.llm_provider)
            formatted_history = self._format_chat_history(chat_history)
            
            # 프롬프트 템플릿을 사용하여 프롬프트 구성
            prompt = self._build_prompt_with_template(message, context, formatted_history, dog_profile_prompt, template_content)
            
            logger.info(f"프롬프트 템플릿 프롬프트 구성 완료, 길이: {len(prompt)}")
            
            # 스트리밍 응답 생성
            full_response = ""
            
            # LangChain chain을 사용한 스트리밍 (프롬프트 템플릿 적용)
            try:
                logger.info("LangChain 프롬프트 템플릿 스트리밍 시작")
                
                # 프롬프트 템플릿을 임시로 설정
                original_template = self.prompt_template.template
                self.prompt_template.template = template_content
                
                # chain에 입력 데이터 준비
                input_data = {
                    "context": context,
                    "question": message,
                    "chat_history": formatted_history,
                    "dog_profile": dog_profile_prompt
                }
                
                # 스트리밍 실행
                async for chunk in self.chain.astream(input_data):
                    if hasattr(chunk, 'content') and chunk.content:
                        chunk_text = chunk.content
                        full_response += chunk_text
                        # SSE 형식으로 데이터 전송
                        yield f"data: {json.dumps({'content': chunk_text, 'done': False})}\n\n"
                    elif isinstance(chunk, str) and chunk.strip():
                        chunk_text = chunk.strip()
                        full_response += chunk_text
                        # SSE 형식으로 데이터 전송
                        yield f"data: {json.dumps({'content': chunk_text, 'done': False})}\n\n"
                
                # 원래 템플릿으로 복원
                self.prompt_template.template = original_template
                
                logger.info("LangChain 프롬프트 템플릿 스트리밍 완료")
                
            except Exception as e:
                # 오류 발생 시에도 원래 템플릿으로 복원
                if hasattr(self, 'prompt_template'):
                    self.prompt_template.template = original_template
                logger.error(f"LangChain 프롬프트 템플릿 스트리밍 중 오류: {str(e)}")
                raise
            
            # 메시지 임베딩 생성
            message_embedding = self.embeddings.encode(message, normalize_embeddings=True)
            
            # 채팅 이력 저장
            chat = DogChat(
                message=message,
                response=full_response,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                dog_id=dog_id,
                uid=pet.uid,
                message_embedding=message_embedding,
                llm_provider="ollama",
                prompt_template_text=template_content
            )
            await self.chats_repo.create_chat(chat)
            
            logger.info("채팅 이력 저장 완료")
            
            # 스트리밍 완료 신호
            yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
            
        except Exception as e:
            logger.error(f"프롬프트 템플릿 스트리밍 채팅 처리 중 오류 발생: {str(e)}")
            error_data = json.dumps({'error': str(e), 'done': True})
            yield f"data: {error_data}\n\n"

    def _build_prompt_with_template(self, message: str, context: str = "", chat_history: str = "", dog_profile_prompt: str = "", template_content: str = "") -> str:
        """프롬프트 템플릿을 사용하여 프롬프트를 구성합니다."""
        # 프롬프트 템플릿에서 변수 치환
        prompt = template_content
        
        # context가 빈 문자열이면 해당 섹션 제거
        if not context or not context.strip():
            prompt = prompt.replace("참고 문서 (한글로 작성됨):\n{{ context }}\n\n", "")
        else:
            prompt = prompt.replace("{{ context }}", context)
            
        # chat_history가 빈 문자열이면 해당 섹션 제거
        if not chat_history or not chat_history.strip():
            prompt = prompt.replace("이전 대화 내용:\n{{ chat_history }}\n\n", "")
        else:
            prompt = prompt.replace("{{ chat_history }}", chat_history)
            
        # 사용자 질문 추가
        prompt = prompt.replace("{{ question }}", message)
        
        # 반려견 프로필 프롬프트 추가
        prompt = prompt.replace("{{ dog_profile }}", dog_profile_prompt)
        
        return prompt.strip() 