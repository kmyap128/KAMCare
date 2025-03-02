import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("AIzaSyDfg8Lp2cYCnpQ0oQ6idmUTebjYEudHthU");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const prompt = "Explain how AI works";

model.generateContent(prompt)
    .then(result => console.log(result.response.text()))
    .catch(error => console.error("Error:", error));
