from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")

template = """

System : You are an expert stock market data analysis.

Can you provide an expert analysis of the provided financial data as follows:

- financial health of the organisation
- is it a good idea to invest in the organisation
- what is the future of the organisation

ONLY RETURN THE MOST IMPORTANT DETAILS ABOUT THE ORGANISATION THAT CAN BE USED AS INDICATORS FOR INVESTING ON THE 
STOCK!!

input text: {text}

"""

prompt = PromptTemplate.from_template(template)

llm_chain = LLMChain(prompt=prompt, llm=llm)


def get_finantial_insights(text):
    return llm_chain.run(text)
