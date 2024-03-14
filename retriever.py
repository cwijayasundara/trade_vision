import os
from dotenv import load_dotenv
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'

persistent_dir = 'chroma_store'

vectorstore = Chroma(persist_directory=persistent_dir,
                     embedding_function=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
    {context}   
    if you can't find the answer, just return "Answer not found in the context"
    Question: {question}
    """
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(model="gpt-4-1106-preview")

output_parser = StrOutputParser()

setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)

chain = (setup_and_retrieval
         | prompt
         | model
         | output_parser)


def vector_db_reader(request):
    response = chain.invoke(request)
    return response


# question = "Whats the total revenue of Tesla ?"
# print(vector_db_reader(question))
