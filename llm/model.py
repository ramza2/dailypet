from sentence_transformers import SentenceTransformer

# 전역 변수로 _model 선언
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('BAAI/bge-m3')
    return _model