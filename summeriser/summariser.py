from dotenv import load_dotenv
from langchain.chains import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI

load_dotenv()


llm = ChatOpenAI(temperature=0,
                 model_name="gpt-4-0125-preview")

chain = load_summarize_chain(llm,
                             chain_type="stuff")


def summarizer(company):
    loader = PyPDFLoader(company)
    document = loader.load()
    summary = chain.run(document)
    return summary
