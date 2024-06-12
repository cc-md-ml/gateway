from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import (
    setup_env, get_env_value
)
from src.langchain.schemas import (
    PromptRequest, PromptResponse
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
        self.system = "You are a helpful dermatologist. You provide information in a structured way."
        self.human = "{text}"
        self.prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", self.human)])

    async def send_prompt(self, body: PromptRequest) -> PromptResponse:
        """
        Sends prompt to groq based on prediction results.
        """
        chain = self.prompt | self.chat
        
        prompt = f"""
        Can you provide me a short brief regarding {body.disease}?
        Please use the following structure with no more than 50 words for each section:
        1. Explanation, explain or describe what is {body.disease}?
        2. Symptoms, what is observable from patients that have {body.disease}?
        3. Treatment, what is the usual treatment protocol for {body.disease}?
        4. Is it common/prevalent? How many cases of {body.disease} are reported every year?
        5. Is it contagious? Answer with only Yes or No! (Answer with only 1 word for this section!)
        """
        
        res = chain.invoke({"text": prompt})
        
        payload = self._make_llm_payload(res.content)
        
        return payload
    
    def _make_llm_payload(self, response: str) -> PromptResponse:
        """
        # TODO
        Structure AIMessage object response into valid PromptResponse model for payload response.
        """
        print(response)
        payload = PromptResponse(
            description="",
            symptoms="",
            contagiousness="",
            treatment="",
            prevalence="",
        )
