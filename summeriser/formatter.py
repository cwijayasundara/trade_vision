from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv()

# llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0125")

template = """

System : You are an expert in stock markets and text formatting to produce executive summaries.

Format the provided text highlighting important information about the provided stock in a way that it is easy to read 
and understand by an investment advisor in point form.

some examples of point form are:

- This is the first important point about the stock
- This is the second point about the stock

ONLY RETURN THE DETAILS IN POINT FORM AND NOTHING ELSE!!

input text: {text}
"""

prompt = PromptTemplate.from_template(template)

llm_chain = LLMChain(prompt=prompt, llm=llm)

st.cache_data


def format_text(text):
    return llm_chain.run(text)
