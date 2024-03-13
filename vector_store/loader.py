import os

from dotenv import load_dotenv
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader

load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'

loader = PyPDFDirectoryLoader('../docs/10-k/')

docs = loader.load()
print(len(docs))

persistent_dir = '../chroma_store'
# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# save the splits
vectorstore = Chroma.from_documents(documents=splits,
                                    persist_directory=persistent_dir,
                                    embedding=OpenAIEmbeddings())

vectorstore.persist()
#  retriever to test if the data is there in the vectorstore
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

response = rag_chain.invoke("What are the Primary Manufacturing Facilities of Tesla?")
print(response)
