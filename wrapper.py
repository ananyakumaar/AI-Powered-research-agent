import os
import google.generativeai as genai
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from dotenv import load_dotenv
from typing import List, Optional, Any
from langchain.tools import Tool

print("Debug: wrapper.py is being imported.")

# 🔑 Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 🤖 Gemini Wrapper for LangChain
class ChatGemini(BaseChatModel):
    model: str = "gemini-2.0-flash"
    temperature: float = 0.2
    tools: List[Tool] = []

    def _llm_type(self) -> str:
        return "google-gemini"

    def _chat(self, messages: List[HumanMessage]) -> str:
        prompt = "\n".join([m.content for m in messages])
        response = genai.GenerativeModel(self.model).generate_content(prompt)
        return response.text

    def _generate(self, messages: List[HumanMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        text = self._chat(messages)
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])

    def bind_tools(self, tools: List[Tool]) -> "ChatGemini":
        """Attach tools to the LLM for function calling."""
        self.tools = tools
        return self
