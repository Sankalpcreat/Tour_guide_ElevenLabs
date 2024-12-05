from langchain_community.llms import ollama
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LangchainService:
    def __init__(self):
        self.llm = OllamaLLM(
            model="llama2:latest",
            base_url="http://localhost:11434",
            temperature=0.7
        )

        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("You are a helpful AI assistant."),
            HumanMessagePromptTemplate.from_template("{prompt}")
        ])

        self.conversation = self.prompt | self.llm
        logger.info("Langchain service initialized successfully")
    
    async def get_response(self, prompt: str) -> str:
        try:
            response = await self.conversation.ainvoke({"prompt": prompt})
            return response
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            return "An error occurred while processing your request."