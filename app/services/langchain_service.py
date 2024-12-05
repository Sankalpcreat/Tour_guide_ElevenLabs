from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import ollama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LangchainService:
    def __init__(self):
        try:
            self.llm = ollama.Ollama(
                model="llama.3.2:latest",
                base_url="http://localhost:11434",
                temperature=0.7
            )
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", "{context}"),
                ("human", "{prompt}")
            ])
            self.conversation = self.prompt | self.llm
            logger.info("LangChain service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing LangChain service: {e}")
            raise

    async def get_response(self, prompt: str, context: str = "") -> str:
        try:
            response = await self.conversation.ainvoke({"context": context, "prompt": prompt})
            return response.content
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            return "I apologize, but I encountered an error processing your request."