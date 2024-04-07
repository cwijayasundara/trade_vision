from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

load_dotenv()


# llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0125")

template = """

System : You are an expert stock market data analysis.

Can you provide an expert analysis of the provided a professional financial on the data covering the below aspects:

- financial health of the organisation
- is it a good idea to invest in the organisation
- what is the future growth of the organisation

MAKE SURE TO PROVIDE A DETAILED ANALYSIS OF THE STOCK BASED ON THE PROVIDED DATA, LIMITING TO THE MOST IMPORTANT 
DETAILS THAT CAN BE USED AS INDICATORS FOR INVESTING ON THE STOCK !!. 

PRODUCE THE OUTPUT IN POINT FORM AND NO MORE THAN 200 WORDS!!

input text: {text}

"""

prompt = PromptTemplate.from_template(template)

llm_chain = LLMChain(prompt=prompt, llm=llm)


def get_finantial_insights(text):
    return llm_chain.run(text)
