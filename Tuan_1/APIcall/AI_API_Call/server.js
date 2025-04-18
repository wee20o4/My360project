const express = require("express");
const axios = require("axios");
const cors = require("cors");
const path = require("path");
require("dotenv").config();

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

app.use(express.static(path.join(__dirname, "public")));

app.post("/translate", async (req, res) => {
  const { text, target_lang } = req.body;

  if (!text || !target_lang) {
    return res
      .status(400)
      .json({ error: "Text and target language are required" });
  }

  try {
    const response = await axios.post(
      "https://api-free.deepl.com/v2/translate",
      {
        text: [text],
        target_lang,
        auth_key: process.env.DEEPL_AUTH_KEY,
      }
    );

    res.json(response.data);
  } catch (error) {
    console.error("Translation error:", error);
    res.status(500).json({ error: "Translation failed" });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
