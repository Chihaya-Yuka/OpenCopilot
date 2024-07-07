let apiKey = getCookie('openai_api_key');
if (apiKey) {
    document.getElementById('api-key').value = apiKey;
}

function saveApiKey() {
    const apiKeyInput = document.getElementById('api-key').value.trim();
    if (!apiKeyInput) {
        alert('Please enter an API Key.');
        return;
    }
    setCookie('openai_api_key', apiKeyInput, 30);
    alert('API Key saved successfully.');
}

function deleteApiKey() {
    setCookie('openai_api_key', '', -1);
    document.getElementById('api-key').value = '';
    alert('API Key deleted.');
}

function setCookie(name, value, days) {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (!userInput) return;

    const apiKey = getCookie('openai_api_key');
    if (!apiKey) {
        alert('Please enter your API Key first.');
        return;
    }

    appendMessage(userInput, 'sent');
    document.getElementById('user-input').value = '';

    fetchResponse(userInput, apiKey)
        .then(response => response.json())
        .then(data => {
            const aiResponse = data.choices[0].text.trim();
            appendMessage(aiResponse, 'received');
        })
        .catch(error => {
            console.error('Error fetching AI response:', error);
            appendMessage('Error fetching AI response. Please try again.', 'received');
        });
}

async function fetchResponse(userInput, apiKey) {
    const baseUrl = 'https://127.0.0.1:2333/v1/engines/davinci-codex/completions';
    const response = await fetch(baseUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            prompt: userInput,
            max_tokens: 150
        })
    });
    return response;
}

function appendMessage(message, type) {
    const messageContainer = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type === 'sent' ? 'sent' : 'received');
    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = message;
    messageElement.appendChild(messageContent);
    messageContainer.appendChild(messageElement);

    messageContainer.scrollTop = messageContainer.scrollHeight;
}
