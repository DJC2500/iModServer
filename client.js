const ws = new WebSocket("ws://localhost:8080");

const username = "akkin";
const recipient = "divine";
const message = "Hello";

ws.onopen = () => {
    console.log("Connected to WebSocket server");
    sendMessage(recipient, message);
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    console.log(`Message from ${msg.sender}: ${msg.content}`);
};

ws.onclose = () => {
    console.log("Disconnected from WebSocket server");
};

function sendMessage(recipient, content) {
    const message = { 
        sender: username, 
        recipient, 
        content, 
        timestamp: new Date().toISOString()
    };
    ws.send(JSON.stringify(message));
    console.log("Message sent!");
}

