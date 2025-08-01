const express = require("express");
const cors = require("cors");
const app = express();
const port = 5000;

// Kết nối Gemini API
const { GoogleGenerativeAI } = require("@google/generative-ai");
const GEMINI_API_KEY = "AIzaSyBld67u3T-_DKfoyLh3WYrr4N2YRGpGYCo"; // hoặc dùng dotenv để bảo mật

const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

app.use(cors());
app.use(express.json());

app.post("/api/chat", async (req, res) => {
  const { message } = req.body;
  console.log("🧑 Người dùng hỏi:", message);

  try {
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });
    const result = await model.generateContent(message);
    const response = result.response;   
    const text = response.text(); 

    res.json({ reply: text });
  } catch (error) {
    console.error("Lỗi Gemini:", error);
    res.status(500).json({ reply: "Xin lỗi, tôi không thể phản hồi lúc này." });
  }
});

app.listen(port, () => {
  console.log(`✅ Server đang chạy tại http://localhost:${port}`);
});
