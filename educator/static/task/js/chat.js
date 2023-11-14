document.addEventListener('DOMContentLoaded', function() {
    const chatList = document.getElementById('chat-list');
    const chatMessages = document.getElementById('chat-messages');

    chatList.addEventListener('click', function(event) {
        const targetChat = event.target.closest('.chat-item');
        if (targetChat) {
            const chatId = targetChat.dataset.chatId;
            loadChatMessages(chatId);
        }
    });

    function loadChatMessages(chatId) {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `/chats/${chatId}/messages/`);
        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const messages = response.messages;
                const chatMessages = document.getElementById('chat-messages');

                chatMessages.innerHTML = ''; // Очищаем контейнер сообщений

                messages.forEach(function(message) {
                    const messageElement = document.createElement('div');
                    messageElement.classList.add('message');
                    messageElement.textContent = `${message.sender}: ${message.content}`;
                    chatMessages.appendChild(messageElement);
                });
            }
        };
        xhr.send();
    }

});


