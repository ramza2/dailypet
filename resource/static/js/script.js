// 전역 변수
let selectedDog = null;
let openaiCursor = null;  // OpenAI 커서
let ollamaCursor = null;  // Ollama 커서
let openaiHasMore = true;  // OpenAI의 hasMore 상태
let ollamaHasMore = true;  // Ollama의 hasMore 상태
const PAGE_SIZE = 10;
const openaiProvider = 'openai';
const ollamaProvider = 'ollama';

/** false면 메인 UI에서 OpenAI 패널이 숨겨지며 이력/전송도 생략됩니다. (#openaiChatPanel 의 hidden 과 맞출 것) */
const OPENAI_CHAT_ENABLED = (() => {
    const panel = document.getElementById('openaiChatPanel');
    return panel != null && !panel.hidden;
})();

// DOM 요소
const openaiMessageInput = document.getElementById('openaiMessageInput');
const openaiSendButton = document.getElementById('openaiSendButton');
const openaiChatOutput = document.getElementById('openaiChatOutput');
const openaiLoadingDialog = document.getElementById('openaiLoadingDialog');

const ollamaMessageInput = document.getElementById('ollamaMessageInput');
const ollamaSendButton = document.getElementById('ollamaSendButton');
const ollamaChatOutput = document.getElementById('ollamaChatOutput');
const ollamaLoadingDialog = document.getElementById('ollamaLoadingDialog');

// 채팅 이력 불러오기 (커서 기반)
async function loadChatHistory(dogId, provider, cursor) {
    try {
        let url = `/chat/history?dog_id=${dogId}&provider=${provider}&page_size=${PAGE_SIZE}`;
        if (cursor) {
            url += `&cursor=${encodeURIComponent(cursor)}`;
        }
        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('채팅 이력 불러오기 실패');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return { chats: [], hasMore: false, nextCursor: null };
    }
}

// 채팅 이력 표시 (커서 기반)
async function displayChatHistory(dogId, provider, cursor, chatOutput) {
    const result = await loadChatHistory(dogId, provider, cursor);
    if (result.chats.length === 0) return result;

    console.log(`${provider} displayChatHistory: cursor=${cursor}, chats.length=${result.chats.length}`);

    // 커서가 있는 경우 (이전 페이지 로드) 기존 메시지 위에 추가
    if (cursor) {
        console.log(`${provider} 이전 히스토리 로드: 스크롤 위치 보존 시작`);
        
        // 현재 스크롤 위치와 전체 높이 저장
        const currentScrollTop = chatOutput.scrollTop;
        const currentScrollHeight = chatOutput.scrollHeight;
        console.log(`${provider} 현재 스크롤 위치: ${currentScrollTop}, 전체 높이: ${currentScrollHeight}`);
        
        const tempDiv = document.createElement('div');
        result.chats.reverse().forEach(chat => {
            appendMessage(chat.role, chat.content, tempDiv);
        });
        chatOutput.insertBefore(tempDiv, chatOutput.firstChild);
        
        // DOM 업데이트 후 스크롤 위치 조정
        requestAnimationFrame(() => {
            const newScrollHeight = chatOutput.scrollHeight;
            const heightDifference = newScrollHeight - currentScrollHeight;
            const newScrollTop = currentScrollTop + heightDifference;
            
            console.log(`${provider} 스크롤 조정: 새 높이=${newScrollHeight}, 높이 차이=${heightDifference}, 새 스크롤 위치=${newScrollTop}`);
            
            chatOutput.scrollTop = newScrollTop;
        });
    } else {
        console.log(`${provider} 첫 페이지 로드: 스크롤을 맨 아래로 이동`);
        // 첫 페이지인 경우 채팅창 초기화 후 추가
        chatOutput.innerHTML = '';
        result.chats.reverse().forEach(chat => {
            appendMessage(chat.role, chat.content, chatOutput);
        });
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    return result;
}

// 스크롤 이벤트 핸들러 (커서 기반)
function setupScrollHandler(chatOutput, provider) {
    let isLoading = false;  // 로딩 중인지 여부를 추적하는 플래그

    chatOutput.addEventListener('scroll', async () => {
        const hasMore = provider === openaiProvider ? openaiHasMore : ollamaHasMore;
        const cursor = provider === openaiProvider ? openaiCursor : ollamaCursor;
        
        // 스크롤이 상단 근처에 있고, 로딩 중이 아니며, 더 많은 데이터가 있고, cursor가 null이 아닐 때만 이전 히스토리 로드
        if (chatOutput.scrollTop <= 50 && !isLoading && hasMore && cursor !== null) {
            console.log(`${provider} 스크롤 이벤트: scrollTop=${chatOutput.scrollTop}, isLoading=${isLoading}, hasMore=${hasMore}, cursor=${cursor}`);
            
            isLoading = true;  // 로딩 시작
            
            try {
                console.log(`${provider} 이전 히스토리 로드 시작: cursor=${cursor}`);
                
                const result = await displayChatHistory(selectedDog, provider, cursor, chatOutput);
                
                // 상태 업데이트
                if (provider === openaiProvider) {
                    openaiHasMore = result.hasMore;
                    openaiCursor = result.nextCursor;
                } else {
                    ollamaHasMore = result.hasMore;
                    ollamaCursor = result.nextCursor;
                }
                
                console.log(`${provider} 이전 히스토리 로드 완료: hasMore=${result.hasMore}, nextCursor=${result.nextCursor}`);
            } finally {
                isLoading = false;  // 로딩 완료
            }
        }
    });
}

// 반려견 선택 처리
async function selectDog(dogId) {
    selectedDog = dogId;
    
    // 모든 프로필에서 selected 클래스 제거
    document.querySelectorAll('.dog-profile').forEach(profile => {
        profile.classList.remove('selected');
    });
    
    // 선택된 프로필에 selected 클래스 추가
    const selectedProfile = document.querySelector(`.dog-profile[onclick="selectDog(${dogId})"]`);
    if (selectedProfile) {
        selectedProfile.classList.add('selected');
    }
    
    // 채팅 입력 활성화
    if (OPENAI_CHAT_ENABLED) {
        openaiMessageInput.disabled = false;
        openaiSendButton.disabled = false;
    }
    ollamaMessageInput.disabled = false;
    ollamaSendButton.disabled = false;
    
    // 채팅창 초기화
    if (OPENAI_CHAT_ENABLED) {
        openaiChatOutput.innerHTML = '';
    }
    ollamaChatOutput.innerHTML = '';
    
    // 커서 초기화
    openaiCursor = null;
    ollamaCursor = null;
    openaiHasMore = true;  // hasMore 상태 초기화
    ollamaHasMore = true;  // hasMore 상태 초기화
    
    // 스크롤 이벤트 핸들러 설정
    if (OPENAI_CHAT_ENABLED) {
        setupScrollHandler(openaiChatOutput, openaiProvider);
    }
    setupScrollHandler(ollamaChatOutput, ollamaProvider);
    
    // 채팅 이력 불러오기 (첫 페이지)
    let openaiResult = { nextCursor: null, hasMore: false };
    if (OPENAI_CHAT_ENABLED) {
        openaiResult = await displayChatHistory(dogId, openaiProvider, null, openaiChatOutput);
    }
    const ollamaResult = await displayChatHistory(dogId, ollamaProvider, null, ollamaChatOutput);
    
    // cursor 설정
    openaiCursor = openaiResult.nextCursor;
    ollamaCursor = ollamaResult.nextCursor;
    openaiHasMore = openaiResult.hasMore;
    ollamaHasMore = ollamaResult.hasMore;
    
    console.log(`첫 페이지 로드 완료: openai=${OPENAI_CHAT_ENABLED}, openaiCursor=${openaiCursor}, ollamaCursor=${ollamaCursor}`);
}

// OpenAI 메시지 전송
async function sendOpenAIMessage() {
    const message = openaiMessageInput.value.trim();
    if (!message || !selectedDog) return;
    
    // 로딩 표시
    openaiLoadingDialog.classList.remove('hidden');
    openaiSendButton.disabled = true;
    openaiMessageInput.disabled = true;

    try {
        const response = await fetch('/openai/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                dog_id: selectedDog,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error('API 호출 실패');
        }

        const data = await response.json();

        // 사용자 메시지 추가
        appendMessage('user', message, 'openaiChatOutput');
        // AI 응답 추가
        appendMessage('assistant', data.response, 'openaiChatOutput');
        
        // 새 메시지 추가 후 스크롤을 맨 아래로 이동
        openaiChatOutput.scrollTop = openaiChatOutput.scrollHeight;

    } catch (error) {
        console.error('Error:', error);
        alert('메시지 전송 중 오류가 발생했습니다.');
    } finally {
        // 로딩 숨기기
        openaiLoadingDialog.classList.add('hidden');
        openaiSendButton.disabled = false;
        openaiMessageInput.disabled = false;
        openaiMessageInput.value = '';
    }
}

// Ollama 메시지 전송 (스트리밍 방식)
async function sendOllamaMessage() {
    const message = ollamaMessageInput.value.trim();
    if (!message || !selectedDog) return;
    
    // 로딩 표시
    ollamaLoadingDialog.classList.remove('hidden');
    ollamaSendButton.disabled = true;
    ollamaMessageInput.disabled = true;

    try {
        // 사용자 메시지 추가
        appendMessage('user', message, 'ollamaChatOutput');
        
        // AI 응답 메시지 컨테이너 생성
        const aiMessageDiv = document.createElement('div');
        aiMessageDiv.className = 'message assistant';
        const responseDiv = document.createElement('div');
        responseDiv.className = 'chat-response';
        aiMessageDiv.appendChild(responseDiv);
        ollamaChatOutput.appendChild(aiMessageDiv);
        
        // 스트리밍 응답 처리
        const response = await fetch('/ollama/chat/stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                dog_id: selectedDog,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error('API 호출 실패');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        let sseLineBuffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (value) {
                sseLineBuffer += decoder.decode(value, { stream: true });
            }
            if (done) {
                sseLineBuffer += decoder.decode();
            }

            const lines = sseLineBuffer.split('\n');
            if (!done) {
                sseLineBuffer = lines.pop() ?? '';
            } else {
                sseLineBuffer = '';
            }

            for (const rawLine of lines) {
                const line = rawLine.replace(/\r$/, '');
                if (!line.startsWith('data: ')) continue;
                try {
                    const data = JSON.parse(line.slice(6));

                    if (data.error) {
                        throw new Error(data.error);
                    }

                    if (data.content) {
                        fullResponse += data.content;
                        // 스트리밍 중에도 마크다운 렌더링
                        responseDiv.innerHTML = marked.parse(fullResponse);
                        ollamaChatOutput.scrollTop = ollamaChatOutput.scrollHeight;
                    }
                } catch (e) {
                    console.error('JSON 파싱 오류:', e);
                }
            }

            if (done) break;
        }
        responseDiv.innerHTML = marked.parse(fullResponse);

    } catch (error) {
        console.error('Error:', error);
        alert('메시지 전송 중 오류가 발생했습니다.');
    } finally {
        // 로딩 숨기기
        ollamaLoadingDialog.classList.add('hidden');
        ollamaSendButton.disabled = false;
        ollamaMessageInput.disabled = false;
        ollamaMessageInput.value = '';
    }
}

function appendMessage(role, content, outputId) {
    const chatOutput = typeof outputId === 'string' ? document.getElementById(outputId) : outputId;
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    if (role === 'assistant') {
        // 마크다운을 HTML로 변환
        const htmlContent = marked.parse(content);
        const responseDiv = document.createElement('div');
        responseDiv.className = 'chat-response';
        responseDiv.innerHTML = htmlContent;
        messageDiv.appendChild(responseDiv);
    } else {
        messageDiv.textContent = content;
    }
    
    chatOutput.appendChild(messageDiv);
}

// 이벤트 리스너
if (OPENAI_CHAT_ENABLED) {
    openaiSendButton.addEventListener('click', sendOpenAIMessage);
    openaiMessageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendOpenAIMessage();
        }
    });
}

ollamaSendButton.addEventListener('click', sendOllamaMessage);
ollamaMessageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendOllamaMessage();
    }
}); 