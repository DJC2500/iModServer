import { WebSocketServer } from "ws";
import { createServer } from "http";
import { MongoClient } from "mongodb";
import dotenv from "dotenv";

dotenv.config();

const client = new MongoClient(process.env.MONGO_URI);

async function connectDB() {
    try {
        await client.connect();
        console.log("Connected to MongoDB");
    } catch (error) {
        console.error("MongoDB connection error:", error);
        process.exit(1);
    }
}

connectDB();

const db = client.db("xChange"); // Change this to your actual DB name
const messagesCollection = db.collection("Messages");

const server = createServer();
const wss = new WebSocketServer({ server });

const clients = new Map(); // Store connected users

wss.on("connection", (ws) => {
    console.log("Client connected");

    ws.on("message", async (data) => {
        const msg = JSON.parse(data.toString());
        console.log("Received:", msg);

        const { sender, recipient, content } = msg;

        if (clients.has(recipient)) {
            clients.get(recipient).send(JSON.stringify({ sender, content }));
        } else {
            await messagesCollection.insertOne({
                sender,
                recipient,
                content,
                timestamp: new Date(),
            });
            console.log("Message saved for offline user");
        }
    });

    ws.on("close", () => {
        console.log("Client disconnected");
        // Remove user from online clients
        clients.forEach((value, key) => {
            if (value === ws) clients.delete(key);
        });
    });
});

server.listen(8080, () => {
    console.log("WebSocket server running on ws://localhost:8080");
});
