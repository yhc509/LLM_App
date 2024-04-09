import * as dotenv from "dotenv";

import { ChatOpenAI } from "@langchain/openai";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { ChatPromptTemplate } from "@langchain/core/prompts";

dotenv.config();

const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a world class technical documentation writer."],
  ["user", "{input}"],
]);
const chatModel = new ChatOpenAI({
  openAIApiKey: process.env.OPENAI_API_KEY
});
const outputParser = new StringOutputParser();
const llmChain = prompt.pipe(chatModel).pipe(outputParser);

var request = "what is LangSmith?";
console.log(request)

var response = await llmChain.invoke({
    input:request
});

console.log(response);