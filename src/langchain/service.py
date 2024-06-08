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
        self.system = "You are a dermatologist and will give treatment recommendations based on the disease prediction."
        self.human = """
        Given the following prediction results, provide detailed information about the main disease, other related diseases (top 3 by probability), the severity of the disease, and treatment recommendations with references.

        Prediction Results:
        Main disease: {main_disease}
        Probability: {main_probability}
        Other diseases: {other_diseases}

        Please include references in your response.
        """
        self.prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", self.human)])

    async def send_prompt(self, main_disease, main_probability, other_diseases) -> str:
        """
        Sends prompt to groq based on prediction results
        """
        prompt_input = {
            "main_disease": main_disease,
            "main_probability": main_probability,
            "other_diseases": other_diseases
        }
        chain = self.prompt | self.chat
        res = chain.invoke(prompt_input)
        return res.content