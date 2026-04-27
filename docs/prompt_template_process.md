1. prompt_template 테이블 생성
prompt를 미리 작성하여 테이블에 등록하고 나중에 채팅시 선택후 프롬프트 템플릿에 반영하여 
각 프롬프트별 채팅 응답의 차이를 보고 싶어
prompt_template 테이블을 만들고 테이블 생성 쿼리 알려줘
entity는 /entity 밑에 생성, repository는 /repository 밑에 생성
repository의 경우 다른 Repository 클래스와 마찬가지로 asyncpg.Pool 타입을 생성자 파라미터로 해

2. prompty_template 목록 조회 및 등록 웹페이지
/resource/template에 prompt_template 목록이 나오고 prompt_template를 입력하여 등록하는 기능이 있는 웹페이지 생성
목록에서 prompt_template 항목 선택시 입력창에 선택한 프롬프트 텍스트를 넣어주어 편집이 용이하게 하고 싶어

그리고 처음 페이지 들어갔을때 빈 입력창의 디폴트 문자열은 

"
너는 반려견 건강 전문가이자 수의사입니다.

- 사용자의 질문에 대해 항상 **자연스러운 한국어 문장**으로 답변해주세요.
- 응답은 **정중하고 상담하는 듯한 구어체**로 작성해 주세요.
- 외래어 사용이 필요한 경우에는 괄호를 사용하여 한글 설명을 함께 제공해 주세요. 예: 스트레스(stress)
- "질문:", "답변:", "키워드:" 등의 메타 문구는 포함하지 마세요.
- 사용자가 이해할 수 있도록 쉬운 문장으로 설명해주세요.

---

반려견 정보:
{dog_profile}

참고 문서 (한글로 작성됨):
{context}

이전 대화 내용:
{chat_history}

사용자의 질문:
{question}

응답:
"
위와 같이 해줘 

/resource/template의 layout.html의 메뉴바 부분에 위의 웹페잊 이동 메뉴 추가해 주고.
main.py에 관련 API 추가해줘

3. prompt_template 반영 채팅 페이지
/ollama/chat.py 에서 chat_with_dog 함수와 비슷한 역할을 하되 prompt_template 테이블에서 선택한 프롬프트 문자열로 프롬프트 템플릿 설정(line 59)에 반영하고 싶어
그래서 /resource/templates에 html 하나 추가하고 그 웹페이지가 하는 일은 index.html과 비슷하게 하되 좌측은  prompt_template 항목의 목록을 보여주고 반려견 프로필 목록을 중간에 보여주고 우측에는 index.html과 비슷하게 Ollama 채팅영역이 있었으면 해
동작은 프롬프트와 반려견 프로필 선택이 완료되면 채팅 입력창 활성화 하고 기존처럼 채팅 입력 또는 엔터하면 main.py에 API 하나 추가해서 호출하고 응답을 출력창에 보여주되 기존 index.html 처럼 채팅 입력후 출력까지 spinner 로딩 다이얼로그가 뜨게 해 주고,
반려견 프로필 선택시에는 이전 채팅 이력을 보여주면돼.

4.위에 추가된 채팅 API 추가 기능
채팅 이력을 등록할때 반영된 프롬프트의 텍스트를 dog_chats에 등록하고 싶어
추가 컬럼 쿼리 알려주고
entity(/entity/dog_chat.py) 와 repository(/repository/dog_chats_repository.py) 수정하여 반영해줘

기존 함수를 수정하거나 하지말고 전부 새로 함수를 만들어줘