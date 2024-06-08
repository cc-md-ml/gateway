from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import (
    setup_env, get_env_value
)
from src.langchain.schemas import (
    PromptRequest
)


# load required env variables
setup_env()


class LangChainService():
    """
    LangChain service class for LLM interactions/requests.
    """

    def __init__(self):
        """
        Groq configurations here
        """
        self.chat = ChatGroq(
            temperature=0, 
            model_name="mixtral-8x7b-32768",
            groq_api_key=get_env_value("GROQ_API_KEY")
        )
        self.system = "You are a dermatologist."
        self.human = "{text}"
        self.prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", self.human)])

    async def send_prompt(self) -> str:
        """
        Sends prompt to groq based on prediction results
        # TODO: define service parameters
        # TODO: structure llm response into payload
        """
        chain = self.prompt | self.chat
        res = chain.invoke({"text": "Explain what is melanoma"})
        print(res.content, type(res), type(res.content))
        return res.content