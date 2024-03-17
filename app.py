import os
import streamlit as st

from retriever import vector_db_reader
from studio_app import execute_autogen_studio
from research_team import trigger_research_team
from util.file_util import read_file
from summeriser.formatter import format_text

k_8_summeries = {
    'Tesla': 'docs/8_k_summaries/Tesla_8_k_summary.txt',
    'Nvidia': 'docs/8_k_summaries/Nvidia_8_k_summary.txt',
    'Alphabet': 'docs/8_k_summaries/Alphabet_8_k_summary.txt'
}

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
st.title("Trade Vision : Trading Reimagined !")
options = ["Tesla", "Alphabet", "Nvidia"]

with st.sidebar:
    option = st.selectbox('Select Company ?', options)
    add_radio = st.radio(
        "What do you want to help with today?",
        ("introduction", "chat-with-10-k", "stock-performance", "market-research", "stock-price-prediction")
    )
if add_radio == "introduction":
    introduction = format_text(read_file("docs/intro/intro.txt"))
    st.write(introduction)

elif add_radio == "chat-with-10-k":
    st.image("images/trade_vision_2.webp", width=200, caption="Trade Vision : Trading Reimagined !",
             use_column_width=False)

    st.markdown(''' :orange[2024 8K File Summery]''', unsafe_allow_html=True)
    k_8_summary = format_text(read_file(k_8_summeries[option]))
    st.write(k_8_summary)

    st.subheader(f"Some important facts about {option} annual financial statement 2023:")

    question_1 = f"What are {option} revenue trends over the past three years?"
    question_2 = f"What is {option} net income and margin trends over the past three years?"
    question_3 = f"What does {option} list as its risk factors, and how have they changed from the previous year?"
    question_4 = (f"How does {option} describe its competitive position and market opportunities in the Management's"
                  f"Discussion and Analysis (MD&A) section?")
    question_5 = f"What are {option} current debt levels, and how do they compare to its assets and equity?"

    result_1 = vector_db_reader(question_1)
    result_1_formatted = format_text(result_1)
    st.markdown(''' :blue[Revenue Trend]''', unsafe_allow_html=True)
    st.write(result_1_formatted)

    result_2 = vector_db_reader(question_2)
    result_2_formatted = format_text(result_2)
    st.markdown(''' :blue[Income and Margin Trends]''', unsafe_allow_html=True)
    st.write(result_2_formatted)

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

    st.markdown(''' :red[Chat with the 10K File !]''', unsafe_allow_html=True)
    request = st.text_area(f"How can I help you with {option} 10-K File 2023 Today?", height=100)
    submit = st.button("submit", type="primary")
    if request and submit:
        chat_result = vector_db_reader(request)
        st.write(chat_result)

# to fix
elif add_radio == "stock-performance":
    stock_queries = [f"",
                     f"Plot a chart of to show {option} stock price movement for the past 5 years? Execute the "
                     f"generated code and save the result to a file named {option}_stock_prices_for_5_years.png",
                     f"Plot a chart of to show {option} stock price movement for the last week? Execute the generated "
                     f"code and Save the result to a file named {option}_stock_prices_for_last_week.png",
                     f"Plot a chart of NVDA and TESLA stock price YTD. Execute the code and save the result to a file "
                     f"named nvda_tesla.png"]
    stock_query = st.selectbox(f'Select {option} stock query ?', stock_queries)
    if stock_query:
        submit = st.button("submit", type="primary")
        if submit:
            chat_result = execute_autogen_studio(stock_query)
            st.write(chat_result)

#  to fix (to show the output in the page)
elif add_radio == "market-research":
    research_queries = [f"Research on news articles about {option} focusing on stock price performance?",
                        f"Research on market research reports {option} stock price predictions for 2024?",
                        f"Write a research report for an investor advising if {option} stock is a buy, sell or hold "
                        f"in 2024?"]
    research_query = st.selectbox(f'Select {option} research query ?', research_queries)
    if research_query:
        submit = st.button("submit", type="primary")
        if submit:
            chat_result = trigger_research_team(research_query)
            st.write(chat_result)

elif add_radio == "stock-price-prediction":
    st.write("Please visit the following link to access the stock price prediction tool")
    st.write("http://localhost:8000/")
    st.write("Thank you for your patience !")