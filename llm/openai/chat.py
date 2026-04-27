import openai
import logging
from typing import List
from entity.dog_chat import DogChat
from repository.pet_repository import PetRepository
from repository.dog_chats_repository import DogChatsRepository
from repository.dog_docs_repository import DogDocsRepository
from repository.dog_meal_repository import DogMealRepository
from repository.dog_snack_repository import DogSnackRepository
from repository.dog_walk_repository import DogWalkRepository
from repository.dog_temperature_repository import DogTemperatureRepository
from repository.pulse_repository import PulseRepository
from repository.respiration_repository import RespirationRepository
from fastapi import HTTPException
from openai import OpenAI
from llm.model import get_model
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)

class OpenAIChatService:
    def __init__(
        self, 
        docs_repo: DogDocsRepository, 
        pet_repo: PetRepository, 
        dog_chats_repo: DogChatsRepository,
        dog_meal_repo: DogMealRepository,
        dog_snack_repo: DogSnackRepository,
        dog_walk_repo: DogWalkRepository,
        dog_temperature_repo: DogTemperatureRepository,
        pulse_repo: PulseRepository,
        respiration_repo: RespirationRepository
    ):
        self.pet_repo = pet_repo
        self.dog_chats_repo = dog_chats_repo
        self.docs_repo = docs_repo
        self.dog_meal_repo = dog_meal_repo
        self.dog_snack_repo = dog_snack_repo
        self.dog_walk_repo = dog_walk_repo
        self.dog_temperature_repo = dog_temperature_repo
        self.pulse_repo = pulse_repo
        self.respiration_repo = respiration_repo
        self.client = OpenAI()
        self.model = get_model()
        self.llm_provider = "openai"

    async def _get_embedding(self, text: str) -> List[float]:
        """텍스트를 임베딩 벡터로 변환합니다."""
        return self.model.encode(text, normalize_embeddings=True).tolist()
    
    async def _get_relevant_docs(self, query: str, k: int = 3) -> List[str]:
        """질문과 관련된 문서를 검색합니다."""
        # 질문의 임베딩 생성
        query_embedding = self.model.encode(query, normalize_embeddings=True)
        
        # 데이터베이스에서 유사한 문서 검색
        similar_docs = await self.docs_repo.search_similar_docs(query_embedding, k)
        return [doc.content for doc in similar_docs]

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
            - 평균 산책 시간: {sum((walk.end_dt - walk.start_dt).total_seconds() / 60 for walk in walks) / len(walks):.1f}분
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

    async def chat_with_dog(self, dog_id: int, message: str) -> str:
        try:
            logger.info(f"채팅 요청 수신: dog_id={dog_id}, message={message}")
            
            # 반려견 프로필 조회
            dog_profile = await self.pet_repo.get_pet(dog_id)
            
            if not dog_profile:
                raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")
            
            logger.info(f"반려견 프로필 조회 완료: {dog_profile.name}")

            # 관련 문서 검색
            relevant_docs = await self._get_relevant_docs(message)
            context = "\n".join(relevant_docs) if relevant_docs else "관련 문서가 없습니다."
            
            # 건강 모니터링 데이터 조회
            health_monitoring_data = await self._get_health_monitoring_data(dog_id)
            
            # 시스템 프롬프트 생성
            size_map = {"L": "대형", "M": "중형", "S": "소형"}
            size_type = size_map.get(dog_profile.classification, "알수없음")
            system_prompt = f"""
            **모든 답변은 한국어로만 제공해야 한다.**

            주의사항:
            - **절대 영어로 답변하지 마라. 반드시 모든 내용은 한국어로만 작성한다.**
            - 예시는 모두 한글로 제공하며, 한글 어휘와 표현을 자연스럽게 사용한다.
            - 영문 단어나 외래어 사용은 최소화하고 반드시 괄호로 설명을 덧붙인다. 예: 스트레스(stress)

            1. **전문 수의사로서의 역할**
            - 사용자로부터 제공받은 반려견의 정보(나이, 체중, 품종, 질병, 증상, 병력 등)를 기반으로 건강 상태를 분석하고,
            - 의심되는 질병을 예측하거나 이미 진단받은 질병에 맞는 관리 방법, 운동법, 식이요법, 약 복용 주의사항 등을 제안한다.
            - 수의학적 지식을 기반으로 과학적, 임상적 근거를 함께 설명한다.
            - 반드시 응급 상황 징후가 있는 경우 구체적으로 어떤 행동을 취해야 하는지도 설명한다.

            2. **건강관리사로서의 역할**
            - 질병 예방 및 건강 유지를 위한 일상 관리법, 정기검진 항목, 계절별 주의사항을 알려준다.
            - 반려견의 나이와 건강 상태에 맞는 영양 밸런스를 갖춘 식단을 설계하고,
            - 운동량, 산책 시간, 놀이 유형까지 일상 루틴을 구성해준다.
            - 반려견의 스트레스, 불안, 사회화 문제 등 행동 문제 개선 팁도 포함시킨다.

            3. **답변 방식**
            - 항상 항목별로 정리하여 명확하게 설명하고,
            - 사용자가 이해하기 쉬운 문장과 함께 전문 용어에는 부가 설명을 추가해줘.
            - 사용자 질문이 불분명할 경우, 필요한 추가 정보를 정중하고 구체적으로 요청해줘.

            이제 사용자로부터 제공받는 반려견 정보를 바탕으로, 건강상태 평가, 질병 예측, 일상관리, 식단 설계, 주의사항 등을 안내하는 수의사 겸 건강관리사로 활동을 시작해.
            반드시 한국어로 답변할 것.

            반려견 정보:
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

            관련 문서:
            {context}
            """
            
            # 이전 대화 이력 조회
            previous_chats = await self.dog_chats_repo.get_recent_chats(dog_id, llm_provider=self.llm_provider)
            
            # 대화 메시지 구성
            messages = [{"role": "system", "content": system_prompt}]
            
            # 이전 대화 이력을 메시지에 추가 (역순으로 추가하여 시간순 정렬)
            for chat in reversed(previous_chats):
                messages.append({"role": "user", "content": chat.message})
                messages.append({"role": "assistant", "content": chat.response})
            
            # 현재 메시지 추가
            messages.append({"role": "user", "content": message})
            
            logger.info("메시지 구성 완료")
            
            # OpenAI API 호출
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                bot_response = response.choices[0].message.content
                logger.info("OpenAI API 응답 수신 완료")
                
                # 메시지 임베딩 생성
                message_embedding = await self._get_embedding(message)
                
                # 채팅 이력 저장
                pet = await self.pet_repo.get_pet(dog_id)
                if not pet:
                    raise HTTPException(status_code=404, detail="반려견 프로필을 찾을 수 없습니다.")
                
                chat = DogChat(
                    message=message,
                    response=bot_response,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    dog_id=dog_id,
                    uid=pet.uid,
                    message_embedding=message_embedding,
                    llm_provider="openai",
                    prompt_template_text=None
                )
                await self.dog_chats_repo.create_chat(chat)
                logger.info("채팅 기록 저장 완료")
                
            except Exception as e:
                logger.error(f"OpenAI API 호출 실패: {str(e)}")
                raise HTTPException(status_code=500, detail="OpenAI API 호출에 실패했습니다.")
            
            return bot_response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"채팅 처리 중 오류 발생: {str(e)}")
            raise HTTPException(status_code=500, detail="채팅 처리 중 오류가 발생했습니다.")