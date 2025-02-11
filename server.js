// require("dotenv").config();
// const express = require("express");
// const WebSocket = require("ws");
// const cors = require("cors");

// const app = express();
// const PORT = process.env.PORT || 3001;

// app.use(cors());
// app.use(express.json());



// app.get("/", (req, res) => {''
//   res.send("WebSocket Server is running...");
// });

// // Create WebSocket server
// const server = require("http").createServer(app);
// const wss = new WebSocket.Server({ server });

// // Handle WebSocket connections
// wss.on("connection", (ws) => {
//   console.log("New client connected");

//   ws.on("message", (message) => {
//     console.log(`Received: ${message}`);

//     // Broadcast message to all connected clients
//     wss.clients.forEach((client) => {
//       if (client.readyState === WebSocket.OPEN) {
//         client.send(message);
//       }
//     });
//   });

//   ws.on("close", () => console.log("Client disconnected"));
// });

// server.listen(PORT, () => console.log(`Server running on port ${PORT}`));


const express = require("express");
const cors = require("cors");

const app = express();
app.use(express.json()); // Enable JSON parsing
app.use(cors()); // Allow requests from the client

// Root endpoint
app.get("/", (req, res) => {
  res.send("REST API Server is running...");
});

// Endpoint to receive and respond
app.post("/moses", (req, res) => {
  const { text } = req.body;
  console.log("Received:", text);
  res.json({ response: `${text} is the GOAT: ` });
});

app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
