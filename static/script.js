(() => {
    let selectedCharacter = localStorage.getItem('selectedCharacter') || '';  // 선택된 캐릭터를 로드

    document.addEventListener('DOMContentLoaded', () => {
        if (selectedCharacter) {
            const selectedButton = document.querySelector(`.character-btn[data-character="${selectedCharacter}"]`);
            if (selectedButton) {
                selectedButton.classList.add('selected');
                applyCharacterPrompt(selectedCharacter);  // 선택된 캐릭터의 프롬프트를 반영
            }
        }
    });

    // 캐릭터 버튼 클릭 시 동작 설정
    document.querySelectorAll('.character-btn').forEach(button => {
        button.addEventListener('click', () => {
            const character = button.getAttribute('data-character');
            if (character !== selectedCharacter) {
                selectedCharacter = character;
                localStorage.setItem('selectedCharacter', selectedCharacter);

                // 기존의 selected 클래스를 제거하고 새로운 선택된 버튼에 추가
                document.querySelectorAll('.character-btn').forEach(btn => btn.classList.remove('selected'));
                button.classList.add('selected');

                // 프롬프트를 즉시 반영
                applyCharacterPrompt(selectedCharacter);
            }
        });
    });
    

    document.getElementById('send-btn').addEventListener('click', async () => {
        const userInput = document.getElementById('user-input').value;
        if (!userInput || !selectedCharacter) {
            alert('캐릭터를 먼저 선택해 주세요.');
            return;
        }

        addMessage(convertMarkdownToHtml(userInput), 'user');  // 마크다운 변환 후 메시지 추가
        document.getElementById('user-input').value = '';

        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: userInput,
                    character: selectedCharacter
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.response) {
                addMessage(convertMarkdownToHtml(data.response), 'ai');  // 마크다운 변환 후 메시지 추가

                // 변환 버튼을 보이게 하고 이벤트 리스너 추가
                const convertBtn = document.getElementById('convert-btn');
                convertBtn.style.display = 'block';
                convertBtn.onclick = () => convertToAudio();
            } else if (data.error) {
                addMessage(convertMarkdownToHtml(`Error: ${data.error}`), 'error');  // 마크다운 변환 후 오류 메시지 추가
            }

        } catch (error) {
            addMessage(convertMarkdownToHtml(`Error: ${error.message}`), 'error');  // 마크다운 변환 후 오류 메시지 추가
        }
    });

    function addMessage(text, sender) {
        const chatBox = document.getElementById('chat-box');
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.innerHTML = text;  // HTML로 변환된 텍스트를 적용
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function applyCharacterPrompt(character) {
        fetch(`/prompts/system_message_${character}.txt`)
            .then(response => response.text())
            .then(promptText => {
                console.log(`Loaded prompt for ${character}:`, promptText);
            })
            .catch(error => {
                console.error(`Failed to load prompt for ${character}:`, error);
            });
    }

    async function convertToAudio() {
        try {
            const response = await fetch('http://127.0.0.1:5000/audio/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const audioBlob = await response.blob();
            const audioURL = URL.createObjectURL(audioBlob);

            const audio = document.getElementById('audio');
            audio.src = audioURL;
            audio.style.display = 'block';
            audio.play();
        } catch (error) {
            console.error('Error converting text to audio:', error);
        }
    }

    // 마크다운 문법 변환
    function convertMarkdownToHtml(text) {
        // Add more comprehensive markdown parsing here if needed.
        let html = text
            .replace(/^###\s(.+)/gm, '<h3>$1</h3>')
            .replace(/^##\s(.+)/gm, '<h2>$1</h2>')
            .replace(/^#\s(.+)/gm, '<h1>$1</h1>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
            .replace(/^- (.+)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)+/g, match => `<ul>${match}</ul>`)
            .replace(/\n\n+/g, '</p><p>')
            .replace(/\n/g, '<br>');
    
        return `<p>${html.trim().replace(/^\n+|\n+$/g, '')}</p>`;
    }
    

})();
