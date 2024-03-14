import os
import streamlit as st

from dotenv import load_dotenv
from retriever import vector_db_reader
from stock_executor import execute_stock_price_analyser
from research_team import trigger_research_team
from util.file_util import read_file
from auto_team import execute_auto_team

load_dotenv()

k_8_summeries = {
    'Tesla': 'docs/8_k_summaries/Tesla_8_k_summary.txt',
    'Nvidia': 'docs/8_k_summaries/Nvidia_8_k_summary.txt',
    'Alphabet': 'docs/8_k_summaries/Alphabet_8_k_summary.txt'
}

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
st.title("Trade Vision : Trading Reimagined !")
st.image("images/trade_vision_2.webp", width=300, caption="Trade Vision : Trading Reimagined !", use_column_width=True)
options = ["Tesla", "Alphabet", "Nvidia"]

with st.sidebar:
    option = st.selectbox('Select Company ?', options)
    add_radio = st.radio(
        "What do you want to help with today?",
        ("chat-with-10-k", "stock-performance", "news-analysis", "buy-sell-hold")
    )
if add_radio == "chat-with-10-k":
    st.write("2024 8K File Summery for ", option)
    st.write(read_file(k_8_summeries[option]))

    st.write(f"Some important facts about {option} annual financial statement 2023:")

    question_1 = f"What are {option} revenue trends over the past three years?"
    question_2 = f"What is {option} net income and margin trends over the past three years?"
    question_3 = f"What does {option} list as its risk factors, and how have they changed from the previous year?"
    question_4 = (f"How does {option} describe its competitive position and market opportunities in the Management's"
                  f"Discussion and Analysis (MD&A) section?")
    question_5 = f"What are {option} current debt levels, and how do they compare to its assets and equity?"

    result_1 = vector_db_reader(question_1)
    st.write(f"Revenue Trends : ", result_1)
    result_2 = vector_db_reader(question_2)
    st.write(f"Income and Margin Trends : ", result_2)
    result_3 = vector_db_reader(question_3)
    st.write(f"Risk Factors : ", result_3)
    result_4 = vector_db_reader(question_4)
    st.write(f"Competitive Position and Market Opportunities: ", result_4)
    result_5 = vector_db_reader(question_5)
    st.write(f"current Debt Levels ", result_5)

    request = st.text_area(f"How can I help you with {option} 10-K File 2023 Today?", height=100)
    submit = st.button("submit", type="primary")
    if request and submit:
        chat_result = vector_db_reader(request)
        st.write(chat_result)

elif add_radio == "stock-performance":
    stock_queries = [f"",
                     f"Draw a graph to show {option} stock price movement for the past 4 years?",
                     f"Draw a graph to show {option} stock price movement for the last week?"]
    stock_query = st.selectbox(f'Select {option} stock query ?', stock_queries)
    if stock_query:
        submit = st.button("submit", type="primary")
        if submit:
            chat_result = execute_stock_price_analyser(stock_query)

elif add_radio == "news-analysis":
    research_queries = [f"",
                        f"Research on news articles about {option} ?",
                        f"Research on market research reports {option} stock price predictions for 2024?"]
    research_query = st.selectbox(f'Select {option} research query ?', research_queries)
    if research_query:
        submit = st.button("submit", type="primary")
        if submit:
            chat_result = trigger_research_team(research_query)
            st.write(chat_result)

elif add_radio == "buy-sell-hold":
    scenario_list = [
        "Generate a team of agents to analyse latest stock price performance  from Yahoo finance and recommend if "
        "a given stock is a buy, sell or a hold"]
    building_task = st.selectbox("Select the building task", scenario_list)
    building_task_desc = st.text_input("Enter the task you want the agents to perform")
    submit = st.button("submit", type="primary")
    if building_task and building_task_desc and submit:
        st.write(execute_auto_team(building_task, building_task_desc))
