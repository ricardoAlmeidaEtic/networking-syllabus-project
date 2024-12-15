const apiUrl = 'http://localhost:5000/api/data';

// Connect to the Flask-SocketIO server
const socket = io('http://localhost:5000');

// Listen for new messages
socket.on('new_message', function (data) {
    console.log('New message received:', data);
    // Display the new message on the page
    const chatWindow = document.querySelector('.chat-window');
    chatWindow.innerHTML += `<div class="message received">
                                <span class="user">New User:</span>
                                <span class="message">${data.value}</span>
                              </div>`;
});

// Function to send a chat message (post data)
async function sendMessage() {
    const message = document.getElementById('messageInput').value;
    const postData = { key: "user", value: message };

    try {
        // Send message as POST request to API
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(postData)
        });

        const result = await response.json();
        console.log('POST response:', result);
        alert(result.message);

        // Display the sent message on the page
        const chatWindow = document.querySelector('.chat-window');
        chatWindow.innerHTML += `<div class="message sent">
                                    <span class="user">You:</span>
                                    <span class="message">${message}</span>
                                  </div>`;

        // Clear the textarea
        document.getElementById('messageInput').value = "";
    } catch (error) {
        console.error('Error posting data:', error);
        alert('Error sending message');
    }
}

// Optional: Function to fetch and display data (GET)
async function fetchData() {
    try {
        const response = await fetch(apiUrl, { method: 'GET' });
        const data = await response.json();
        console.log('GET response:', data);
        alert('Data fetched: ' + JSON.stringify(data));
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}