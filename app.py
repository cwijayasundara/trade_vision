import os
import streamlit as st
import pandas as pd
import numpy as np

from retriever import vector_db_reader
from studio_app import execute_autogen_studio
from research_team import trigger_research_team
from util.file_util import read_file
from summeriser.formatter import format_text

from market_info.yfinance_wrapper import (get_stock_info, get_income_statement, show_news, extract_future_outlook)

k_8_summeries = {
    'Tesla': 'docs/k_8_sum/tesla_8_k_summary.txt',
    'Nvidia': 'docs/k_8_sum/nvidia_8_k_summary.txt',
    'Alphabet': 'docs/k_8_sum/alphabet_8_k_summary.txt'
}

ticker_map = {
    'Tesla': 'TSLA',
    'Nvidia': 'NVDA',
    'Alphabet': 'GOOGL'
}

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
st.title("Trade Vision : Trading Reimagined !")
options = ["Tesla", "Alphabet", "Nvidia"]

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image("images/trade_vision_2.webp")
    option = st.selectbox('Select Company ?', options)
    add_radio = st.radio(
        "What do you want to help with today?",
        ("stock highlights !", "highlights-from-knowledge-base", "chat-with-knowledge-base",
         "stock-performance: autogen",
         "market-research: autogen", "stock-price-prediction: taskweaver", "buy-sell-hold: crewai", "about trade vision")
    )

if add_radio == "stock highlights !":
    st.markdown(''' :orange[For stock analysis pls follow the below link !]''', unsafe_allow_html=True)
    st.write("http://localhost:8501/")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["company info", "historical stock prices ", "income statement", "news",
         "future outlook"])

    with tab1:
        if option == "Tesla":
            st.write("Nasdaq: TSLA")
            st.image("images/tsla_pred.png", use_column_width=True)
        elif option == "Nvidia":
            st.write("Nasdaq: NVDA")
            st.image("images/nvda_pred.png", use_column_width=True)
        elif option == "Alphabet":
            st.write("Nasdaq: GOOGL")
            st.image("images/googl_pred.png", use_column_width=True)
        stock_info = get_stock_info(ticker_map[option])
        st.write(stock_info)
    with tab2:
        chart_data = pd.DataFrame(np.random.randn(20, 1), columns=["a"])
        st.line_chart(chart_data)

    with tab3:
        income_statement = get_income_statement(ticker_map[option])
        st.write(income_statement)

    with tab4:
        news = show_news(ticker_map[option])
        st.write(news)
    with tab5:
        recommendations = extract_future_outlook(ticker_map[option])
        st.write(recommendations)

elif add_radio == "highlights-from-knowledge-base":

    st.markdown(''' :orange[Knowledge Base : Summary]''', unsafe_allow_html=True)
    k_8_summary = format_text(read_file(k_8_summeries[option]))
    st.write(k_8_summary)

    st.subheader(f"Some important facts about {option} annual financial statement 2023:")

    question_1 = f"What are {option} revenue trends over the past three years?"
    question_2 = f"What is {option} net income and margin trends over the past three years?"
    question_3 = f"What does {option} list as its risk factors, and how have they changed from the previous year?"
    question_4 = (f"How does {option} describe its competitive position and market opportunities in the Management's"
                  f"Discussion and Analysis (MD&A) section?")
    question_5 = f"What are {option} current debt levels, and how do they compare to its assets and equity?"

    col1, col2 = st.columns(2)

    with col1:
        result_1 = vector_db_reader(question_1)
        result_1_formatted = format_text(result_1)
        st.markdown(''' :blue[Revenue Trend]''', unsafe_allow_html=True)
        st.write(result_1_formatted)

        result_2 = vector_db_reader(question_2)
        result_2_formatted = format_text(result_2)
        st.markdown(''' :blue[Income and Margin Trends]''', unsafe_allow_html=True)
        st.write(result_2_formatted)

    with col2:
        result_3 = vector_db_reader(question_3)
        result_3_formatted = format_text(result_3)
        st.markdown(''' :blue[Risk Factors]''', unsafe_allow_html=True)
        st.write(result_3_formatted)

        result_4 = vector_db_reader(question_4)
        result_4_formatted = format_text(result_4)
        st.markdown(''' :blue[Competitive Position and Market Opportunities]''', unsafe_allow_html=True)
        st.write(result_4_formatted)

    result_5 = vector_db_reader(question_5)
    result_5_formatted = format_text(result_5)
    st.markdown(''' :blue[Current Debt Levels]''', unsafe_allow_html=True)
    st.write(result_5_formatted)

elif add_radio == "chat-with-knowledge-base":
    st.markdown(''' :blue[Chat with the Knowledge Base !]''', unsafe_allow_html=True)
    st.image("images/rag.webp", width=400)
    request = st.text_area(f"How can I help you with {option} knowledge base today?", height=100)
    submit = st.button("submit", type="primary")
    if request and submit:
        chat_result = vector_db_reader(request)
        st.write(format_text(chat_result))

elif add_radio == "stock-performance: autogen":
    st.image("images/autogen_2.png", use_column_width=True)
    stock_queries = [f"",
                     f"Plot a chart of to show {option} stock price movement for the past 5 years? Execute the "
                     f"generated code and save the result to a file named {option}_stock_prices_for_5_years.png",
                     f"Plot a chart of to show {option} stock price movement for the last week? Execute the generated "
                     f"code and Save the result to a file named {option}_stock_prices_for_last_week.png",
                     f"Plot a chart of NVDA and TESLA stock price YTD. Execute the code and save the result to a file "
                     f"named nvda_tesla.png"]

    manual_mode = st.checkbox("manual mode")
    if manual_mode:
        stock_query_manual = st.text_input("How can I help you today?")
        st.write("E.g. Plot a graph to compare the stock price movement of the top 10 tech companies for the past 5 "
                 "years?")
        submit = st.button("submit", type="primary")
        if stock_query_manual and submit:
            chat_result = execute_autogen_studio(stock_query_manual)
            st.write(chat_result)
    else:
        stock_query = st.selectbox(f'Select {option} stock query ?', stock_queries)
        if stock_query:
            submit = st.button("submit", type="primary")
            if submit:
                chat_result = execute_autogen_studio(stock_query)
                st.write(chat_result)

elif add_radio == "market-research: autogen":
    st.image("images/autogen_2.png", use_column_width=True)
    research_queries = [f"Research on news articles about {option} focusing on stock price performance?",
                        f"Research on market research reports {option} stock price predictions for 2024?",
                        f"Write a research report for an investor advising if {option} stock is a buy, sell or hold "
                        f"in 2024?"]
    manual_mode = st.checkbox("manual mode")
    if manual_mode:
        research_query_manual = st.text_input("How can I help you today?")
        st.write("E.g. Research on news articles about Tesla focusing on stock price performance?")
        submit = st.button("submit", type="primary")
        if research_query_manual and submit:
            chat_result = trigger_research_team(research_query_manual)
            st.write(chat_result)
    else:
        research_query = st.selectbox(f'Select {option} research query ?', research_queries)
        submit = st.button("submit", type="primary")
        if research_query and submit:
            chat_result = trigger_research_team(research_query)
            st.write(chat_result)

elif add_radio == "stock-price-prediction: taskweaver":
    st.image("images/task_weaver_2.png", use_column_width=True)
    st.write("Please visit the following link to access the stock price prediction tool")
    st.write("http://localhost:8000/")

elif add_radio == "buy-sell-hold: crewai":
    st.image("images/crew_ai.png", use_column_width=True)
    st.subheader(f"Crew AI Market Analysis: {option}")
    if option == "Tesla":
        analysis = read_file("docs/crew_ai/tesla_output.txt")
        st.write(format_text(analysis))
    elif option == "Alphabet":
        analysis = read_file("docs/crew_ai/google_output.txt")
        st.write(format_text(analysis))
    elif option == "Nvidia":
        analysis = read_file("docs/crew_ai/nvda_output.txt")
        st.write(format_text(analysis))
elif add_radio == "about trade vision":
    st.write("Trade Vision is a tool that provides insights into stock market data, financial reports, and market "
             "research. It is designed to help investors make informed decisions about their investments. Trade Vision "
             "uses a combination of natural language processing, machine learning, and data analysis to provide "
             "actionable insights and recommendations. Whether you are a seasoned investor or new to the stock market, "
             "Trade Vision can help you navigate the complexities of the financial markets and make better investment "
             "decisions.")
    tab1, tab2 = st.tabs(
        ["using gen ai for stock market analysis", "design"])
    with tab1:
        introduction = format_text(read_file("docs/intro/intro.txt"))
        st.write(introduction)
    with tab2:
        st.write("under construction !")

