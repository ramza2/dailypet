// 전역 변수
let selectedDog = null;
let selectedTemplate = null;
let currentCursor = null;  // 커서 기반 페이지네이션
let hasMore = true;
const PAGE_SIZE = 10;
const provider = 'ollama';  // 프롬프트 채팅은 ollama만 사용

/** 이전 페이지(스크롤 업) 로드 중 — 중복 리스너·동시 요청 방지 */
let scrollHistoryLoadInProgress = false;
/** 스크롤 리스너는 한 번만 등록 */
let promptChatScrollListenerAttached = false;

// DOM 요소
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const chatOutput = document.getElementById('chat-messages');
const loadingDialog = document.getElementById('loadingDialog');
const templateSection = document.getElementById('template-section');
const templateToggle = document.getElementById('template-toggle');
const profileSection = document.getElementById('profile-section');
const profileToggle = document.getElementById('profile-toggle');

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

    console.log(`prompt displayChatHistory: cursor=${cursor}, chats.length=${result.chats.length}`);

    // 커서가 있는 경우 (이전 페이지 로드) 기존 메시지 위에 추가
    if (cursor) {
        console.log(`prompt 이전 히스토리 로드: 스크롤 위치 보존 시작`);
        
        // 현재 스크롤 위치와 전체 높이 저장
        const currentScrollTop = chatOutput.scrollTop;
        const currentScrollHeight = chatOutput.scrollHeight;
        console.log(`prompt 현재 스크롤 위치: ${currentScrollTop}, 전체 높이: ${currentScrollHeight}`);
        
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
            
            console.log(`prompt 스크롤 조정: 새 높이=${newScrollHeight}, 높이 차이=${heightDifference}, 새 스크롤 위치=${newScrollTop}`);
            
            chatOutput.scrollTop = newScrollTop;
        });
    } else {
        console.log(`prompt 첫 페이지 로드: 스크롤을 맨 아래로 이동`);
        // 첫 페이지인 경우 채팅창 초기화 후 추가
        chatOutput.innerHTML = '';
        result.chats.reverse().forEach(chat => {
            appendMessage(chat.role, chat.content, chatOutput);
        });
        // 스크롤을 최하단으로 이동
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    return result;
}

// 스크롤 이벤트 핸들러 (커서 기반) — 리스너는 단일 등록
async function onPromptChatScroll() {
    if (!selectedDog) return;
    // 스크롤바가 없을 때 scrollTop 이 0이라 상단 조건이 오동작하는 것을 막음
    if (chatOutput.scrollHeight <= chatOutput.clientHeight + 2) return;
    if (chatOutput.scrollTop > 50 || scrollHistoryLoadInProgress || !hasMore || currentCursor === null) {
        return;
    }

    scrollHistoryLoadInProgress = true;
    try {
        console.log(`prompt 이전 히스토리 로드 시작: cursor=${currentCursor}`);
        const result = await displayChatHistory(selectedDog, provider, currentCursor, chatOutput);
        hasMore = result.hasMore;
        currentCursor = result.nextCursor;
        console.log(`prompt 이전 히스토리 로드 완료: hasMore=${result.hasMore}, nextCursor=${result.nextCursor}`);
    } finally {
        scrollHistoryLoadInProgress = false;
    }
}

function ensurePromptChatScrollListener() {
    if (promptChatScrollListenerAttached) return;
    chatOutput.addEventListener('scroll', onPromptChatScroll);
    promptChatScrollListenerAttached = true;
}

// 템플릿 선택 처리
function selectTemplate(templateId) {
    selectedTemplate = templateId;
    
    // 모든 템플릿에서 selected 클래스 제거
    document.querySelectorAll('.template-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // 선택된 템플릿에 selected 클래스 추가
    const selectedItem = document.querySelector(`.template-item[data-id="${templateId}"]`);
    if (selectedItem) {
        selectedItem.classList.add('selected');
    }
    
    updateChatInputState();
}

// 반려견 선택 처리
async function selectDog(dogId) {
    selectedDog = dogId;
    
    // 모든 프로필에서 selected 클래스 제거
    document.querySelectorAll('.profile-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // 선택된 프로필에 selected 클래스 추가
    const selectedItem = document.querySelector(`.profile-item[data-id="${dogId}"]`);
    if (selectedItem) {
        selectedItem.classList.add('selected');
    }
    
    // 채팅창 초기화
    chatOutput.innerHTML = '';
    currentCursor = null;  // 커서 초기화
    hasMore = true;
    
    // 채팅 이력 로드 (첫 페이지)
    const result = await displayChatHistory(dogId, provider, null, chatOutput);
    currentCursor = result.nextCursor;
    hasMore = result.hasMore;
    
    console.log(`prompt 첫 페이지 로드 완료: cursor=${currentCursor}, hasMore=${hasMore}`);
    
    updateChatInputState();

    ensurePromptChatScrollListener();
}

// 채팅 입력 상태 업데이트
function updateChatInputState() {
    if (selectedDog && selectedTemplate) {
        messageInput.disabled = false;
        sendButton.disabled = false;
    } else {
        messageInput.disabled = true;
        sendButton.disabled = true;
    }
}

// 로딩 표시 (메인 페이지와 동일: CSS absolute, 채팅 섹션 기준)
function showLoading() {
    loadingDialog.classList.remove('hidden');
}

function hideLoading() {
    loadingDialog.classList.add('hidden');
}

// 메시지 전송 (스트리밍 방식)
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || !selectedDog || !selectedTemplate) return;
    
    // 로딩 표시
    showLoading();
    sendButton.disabled = true;
    messageInput.disabled = true;

    try {
        // 사용자 메시지 추가
        appendMessage('user', message, chatOutput);
        
        // AI 응답을 위한 메시지 div 생성
        const assistantMessageDiv = document.createElement('div');
        assistantMessageDiv.className = 'message assistant';
        const responseDiv = document.createElement('div');
        responseDiv.className = 'chat-response';
        assistantMessageDiv.appendChild(responseDiv);
        chatOutput.appendChild(assistantMessageDiv);
        
        // 스트리밍 응답 처리
        const response = await fetch('/api/prompt_chat/stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                dog_id: selectedDog,
                template_id: selectedTemplate,
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
                        chatOutput.scrollTop = chatOutput.scrollHeight;
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
        hideLoading();
        sendButton.disabled = false;
        messageInput.disabled = false;
        messageInput.value = '';
    }
}

function appendMessage(role, content, container) {
    const chatOutput = typeof container === 'string' ? document.getElementById(container) : container;
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

// 템플릿 영역 접기/펼치기
function toggleTemplateSection() {
    const isCollapsed = templateSection.classList.toggle('collapsed');
    templateToggle.textContent = isCollapsed ? '▶' : '▼';
    templateToggle.title = isCollapsed ? '템플릿 영역 펼치기' : '템플릿 영역 접기';
}

// 프로필 영역 접기/펼치기
function toggleProfileSection() {
    const isCollapsed = profileSection.classList.toggle('collapsed');
    profileToggle.textContent = isCollapsed ? '▶' : '▼';
    profileToggle.title = isCollapsed ? '프로필 영역 펼치기' : '프로필 영역 접기';
}

// 이벤트 리스너
document.addEventListener('DOMContentLoaded', function() {
    // 템플릿 선택 이벤트
    const templateItems = document.querySelectorAll('.template-item');
    templateItems.forEach(item => {
        item.addEventListener('click', function() {
            selectTemplate(this.getAttribute('data-id'));
        });
    });

    // 강아지 프로필 선택 이벤트
    const profileItems = document.querySelectorAll('.profile-item');
    profileItems.forEach(item => {
        item.addEventListener('click', function() {
            selectDog(this.getAttribute('data-id'));
        });
    });

    // 메시지 전송 이벤트
    const chatForm = document.getElementById('chat-form');
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });

    // 템플릿 영역 접기/펼치기 이벤트
    templateToggle.addEventListener('click', toggleTemplateSection);

    // 프로필 영역 접기/펼치기 이벤트
    profileToggle.addEventListener('click', toggleProfileSection);
}); 