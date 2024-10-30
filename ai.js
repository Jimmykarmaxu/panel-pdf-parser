import OpenAI from 'openai';
import dotenv from 'dotenv';
dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});


const chatCompletion = await openai.chat.completions.create({
  messages: [
    {
      role: 'user',
      content: 'how can I optimize nodejs app performance',
    },
  ],
  model: 'gpt-4',
});

console.log(chatCompletion.choices);

