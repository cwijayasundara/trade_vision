from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0125")


template_1 = """

System : You are an expert in analysing sentiment from a provided news article heading.

Could you provide the sentiment analysis of the provided news article heading as follows:

- article heading, sentiment

if sentiment is positive then return 1, if sentiment is neutral then return 0, if sentiment is negative then return -1


ONLY RETURN THE ARTICLE HEADING AND THE SENTIMENT IN POINT DICT AND NOTHING ELSE!!

input text: {text}

"""

template_2 = """

System : You are an expert in analysing sentiment from a provided news article heading.

Could you provide an executive interpretation of for the passed data in the following format:

input : List of article headings and their sentiment:

executive interpretation should be in the following format:

if there are more positives 1s than negatives -1s then return "The sentiment is positive"
else if there are more negatives -1s than positives 1s then return "The sentiment is negative"
else return "The sentiment is neutral"


ONLY RETURN THE executive interpretation!!

input text: {text}

"""

prompt_1 = PromptTemplate.from_template(template_1)

llm_chain_1 = LLMChain(prompt=prompt_1, llm=llm)


def analyse_sentiment(text):
    return llm_chain_1.run(text)


prompt_2 = PromptTemplate.from_template(template_2)

llm_chain_2 = LLMChain(prompt=prompt_2, llm=llm)


def analyse_sentiment_list(text_list):
    return llm_chain_2.run(text_list)
