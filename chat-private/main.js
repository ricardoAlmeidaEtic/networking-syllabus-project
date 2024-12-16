const socket = io('http://localhost:5000');

let name = prompt("")

socket.on('new_message', (message) => {
    console.log('New message received:', message);
    if(message.user !== name){
        const chatWindow = document.querySelector('.chat-window');
        chatWindow.innerHTML += `
        <div class="message received">
            <span class="user">${message.user}:</span>
            <span class="message">${message.message}</span>
        </div>`;
    }
});

socket.on('connect', () => {
    console.log('Connected to the Socket.IO server');
});

socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
});

const sendMessage = async () => {
    const message = document.getElementById('messageInput').value;
    const postData = { user: name, message: message };

    try {
        console.log('Sending payload:', postData);

        const response = await fetch('http://localhost:5000/api/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(postData)  // Ensure the payload is properly serialized
        });

        const result = await response.json();
        console.log('POST response:', result);

        if (response.ok) {
            const chatWindow = document.querySelector('.chat-window');
            chatWindow.innerHTML += `<div class="message sent">
                                        <span class="user">You:</span>
                                        <span class="message">${message}</span>
                                      </div>`;
            document.getElementById('messageInput').value = "";
        } else {
            alert(`Server error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error posting message:', error);
        alert('Error sending message');
    }
};
