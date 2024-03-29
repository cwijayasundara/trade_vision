from dotenv import load_dotenv
from langchain.chains import load_summarize_chain, LLMChain, StuffDocumentsChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI

from langchain_community.llms import Ollama

load_dotenv()

llm = Ollama(model="mixtral:instruct", temperature=0)

# llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")

chain = load_summarize_chain(llm, chain_type="stuff")


def summarizer(company):
    loader = PyPDFLoader(company)
    document = loader.load()
    summary = chain.run(document)
    return summary


def summariser_point_form(company):

    prompt_template = """System: You are an expert in stock markets and trading and summarizing stock market and 
    stock related text for executive summary format.

        Write a concise summary of the following in point form:

        "{text}"

        Make sure to keep the summary under 200 words!

        CONCISE SUMMARY:
        """

    prompt = PromptTemplate.from_template(prompt_template)

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain,
                                      document_variable_name="text")

    loader = PyPDFLoader(company)
    docs = loader.load()
    return stuff_chain.run(docs)


def text_summarizer(context):
    prompt_template = """
            System: You are an expert in stock markets and trading and summarizing text for executive summary format.

            Write a concise summary of the following in point form:

            "{text}"

            Make sure to keep the summary under 200 words!

            CONCISE SUMMARY:"""

    prompt = PromptTemplate.from_template(prompt_template)

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain,
                                      document_variable_name="text")
    return stuff_chain.invoke(context)
