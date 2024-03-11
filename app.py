import os
import streamlit as st
from dotenv import load_dotenv
from vector_store.retriever import vector_db_reader
from summeriser.summariser import summarizer

load_dotenv()

documents = {
    'Tesla': 'docs/k_8/tsla-20240102-gen.pdf',
    'Nvidia': 'docs/k_8/6498cd48-aa46-4547-bcd9-061f74e17c4e.pdf',
    'Alphabet': 'docs/k_8/7f7120e075a47cf9e0aa0d9c3607227a.pdf'
}

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'

st.title("Trade Vision : Trading Reimagined !")

options = ["Tesla", "Alphabet", "Nvidia"]

with st.sidebar:
    option = st.selectbox('Select Company ?', options)
    add_radio = st.radio(
        "What do you want to help with today?",
        ("chat", "latest-stock-price-performance", "news_analysis", "buy-sell-hold")
    )
if add_radio == "chat":
    st.write("Summarizing the 8-K File for", option)
    st.write(summarizer(documents[option]))

    st.write(f"Some important facts about {option} 10-K File 2023:")
    question_1 = f"Whats the total revenue of {option} ?"
    question_2 = f"What are the main products and services of {option} given in the 10-K file?"
    question_3 = f"Who are the main competitors of {option} given in the 10-K file?"
    question_4 = f"What are the new innovations of {option} given in the 10-K file?"
    question_5 = f"What are the main risks of {option} given in the 10-K file?"

    result_1 = vector_db_reader(question_1)
    st.write(f"Total revalue of {option} is : ", result_1)
    result_2 = vector_db_reader(question_2)
    st.write(f"Main products and services of {option} are : ", result_2)
    result_3 = vector_db_reader(question_3)
    st.write(f"Main competitors of {option} are : ", result_3)
    result_4 = vector_db_reader(question_4)
    st.write(f"New innovations of {option} are : ", result_4)
    result_5 = vector_db_reader(question_5)
    st.write(f"Main risks of {option} are : ", result_5)

    request = st.text_area(f"How can I help you with {option} 10-K File 2023 Today?", height=100)
    submit = st.button("submit", type="primary")
    if request and submit:
        chat_result = vector_db_reader(request)
        st.write(chat_result)
elif add_radio == "latest-stock-price-performance":
    st.write("This feature is under development")
elif add_radio == "news_analysis":
    st.write("This feature is under development")
elif add_radio == "buy-sell-hold":
    st.write("This feature is under development")
