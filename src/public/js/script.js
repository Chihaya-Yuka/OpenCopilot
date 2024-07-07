function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'sent');
    document.getElementById('user-input').value = '';

    fetchResponse(userInput)
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

async function fetchResponse(userInput) {
    const baseUrl = `http://127.0.0.1:2333/aigc/claude-3.5-sonnet?question=${encodeURIComponent(userInput)}`;
    const response = await fetch(baseUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
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
