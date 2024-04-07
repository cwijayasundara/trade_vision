import os
import streamlit as st
import yfinance as yf
from datetime import datetime

from retriever import vector_db_reader
from research_team import trigger_research_team
from util.file_util import read_file
from summeriser.formatter import format_text
from news_analysis.news_analysis import get_news_for_ticker, analyse_sentiment_df
from finance_analyser.finance_analyser import get_finantial_insights
from market_info.yfinance_wrapper import (get_stock_info, get_income_statement, extract_future_outlook)
from risk_simulation import construct_simulation
from stock_investigator import trigger_code_executor_agent
from stock_price_pred.streamlit_stock_pred import predict_stock_price

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
    option = st.selectbox('Select Company !', options)
    add_radio = st.radio(
        "What can I do for you today?",
        ("stock highlights !",
         "highlights-from-knowledge-base",
         "chat-with-knowledge-base",
         "tools: stock price investigator",
         "tools: market research",
         "tools: stock predictions",
         "tools: monte carlo simulation",
         "final report",
         "about trade vision")
    )

if add_radio == "stock highlights !":

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["company info", "stock prices ", "financials", "news", "future outlook"])

    selected_stock = ticker_map[option]
    stock_data = yf.Ticker(selected_stock)

    with tab1:
        st.subheader("""Nasdaq price prediction for """ + selected_stock)

        if option == "Tesla":
            st.image("images/tsla_pred.png", use_column_width=True)
        elif option == "Nvidia":
            st.image("images/nvda_pred.png", use_column_width=True)
        elif option == "Alphabet":
            st.image("images/googl_pred.png", use_column_width=True)

        predict_stock_price(selected_stock)
        stock_info = get_stock_info(ticker_map[option])
        st.subheader("""Company **info** for """ + selected_stock)
        st.write(get_finantial_insights(stock_info))

    with tab2:

        tab15, tab16, tab17 = st.tabs(["daily closing price", "today's closing price", "stock actions"])

        with tab15:
            st.subheader("""Daily **closing price** for """ + selected_stock)
            stock_df = stock_data.history(period='1d', start='2020-01-01',
                                          end=None)
            st.line_chart(stock_df.Close)
            daily_stock_analysis = get_finantial_insights(stock_df.Close)
            st.write(daily_stock_analysis)

        with tab16:

            st.subheader("""Last **closing price** for """ + selected_stock)
            today = datetime.today().strftime('%Y-%m-%d')
            stock_lastprice = stock_data.history(period='1d', start=today, end=today)
            last_price = stock_lastprice.Close
            if last_price.empty:
                st.write("No data available at the moment")
            else:
                st.write(last_price)
                last_price_analysis = get_finantial_insights(last_price)
                st.write(last_price_analysis)
        with tab17:

            st.subheader("""Stock **actions** for """ + selected_stock)
            display_action = stock_data.actions
            if display_action.empty:
                st.write("No data available at the moment")
            else:
                st.write(display_action)
                action_analysis = get_finantial_insights(display_action)
                st.write(action_analysis)

    with tab3:

        tab10, tab11, tab12, tab13, tab14 = st.tabs(
            ["income statement", "quarterly financials", "institutional investors",
             "quarterly balance sheet", "quarterly cashflow"])

        with tab10:
            st.subheader("""**Income Statement** for """ + selected_stock)
            income_statement = get_income_statement(ticker_map[option])
            st.write(income_statement)

            income_stmt_analysis = get_finantial_insights(income_statement)
            st.write(income_stmt_analysis)
        with tab11:
            st.subheader("""**Quarterly financials** for """ + selected_stock)
            display_financials = stock_data.quarterly_financials
            if display_financials.empty:
                st.write("No data available at the moment")
            else:
                st.write(display_financials)
                finantials_analysis = get_finantial_insights(display_financials)
                st.write(finantials_analysis)
        with tab12:
            st.subheader("""**Institutional investors** for """ + selected_stock)
            display_shareholders = stock_data.institutional_holders
            if display_shareholders.empty:
                st.write("No data available at the moment")
            else:
                st.write(display_shareholders)
                institutional_analysis = get_finantial_insights(display_shareholders)
                st.write(institutional_analysis)
        with tab13:
            st.subheader("""**Quarterly balance sheet** for """ + selected_stock)
            display_balancesheet = stock_data.quarterly_balance_sheet
            if display_balancesheet.empty:
                st.write("No data available at the moment")
            else:
                st.write(display_balancesheet)
                quarterly_balance_analysis = get_finantial_insights(display_balancesheet)
                st.write(quarterly_balance_analysis)
        with tab14:
            st.subheader("""**Quarterly cashflow** for """ + selected_stock)
            display_cashflow = stock_data.quarterly_cashflow
            if display_cashflow.empty:
                st.write("No data available at the moment")
            else:
                st.write(display_cashflow)
                cashflow_analysis = get_finantial_insights(display_cashflow)
                st.write(cashflow_analysis)

    with tab4:
        st.subheader("""Latest news for """ + selected_stock + " from www.finviz.com")
        news = get_news_for_ticker(ticker_map[option])
        st.write(news)
        sentiment = analyse_sentiment_df(news)
        st.subheader(sentiment)

    with tab5:
        st.subheader("""Future outlook for """ + selected_stock)
        recommendations = extract_future_outlook(ticker_map[option])
        st.write(recommendations)

        st.subheader("""**Analysts recommendation** for """ + selected_stock)
        display_analyst_rec = stock_data.recommendations
        if display_analyst_rec.empty:
            st.write("No data available at the moment")
        else:
            st.write(get_finantial_insights(display_analyst_rec))

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

elif add_radio == "tools: stock price investigator":
    st.image("images/trade_vision_1.webp", width=400)
    st.markdown(''' :orange[Visit http://localhost:8081 for interactive investigative tool !]''',
                unsafe_allow_html=True)
    image_name = st.text_input("Enter the image name to save the plot", "stock_prices.png")
    image_location_str = "Execute the generated code and save the result to a file named " + image_name
    stock_queries = [f"",
                     f"Plot a chart of to show {option} stock price movement for the past 5 years? "
                     f"{image_location_str}",
                     f"Plot a chart of to show {option} stock price movement for the last week? {image_location_str}",
                     f"Plot a chart of NVDA and TESLA stock price YTD. {image_location_str}", ]
    manual_mode = st.checkbox("manual mode")
    if manual_mode:
        stock_query_manual = st.text_input("How can I help you today?")
        st.write("E.g. Plot a graph to compare the stock price movement of the top 10 tech companies for the past 5 "
                 "years?")
        submit = st.button("submit", type="primary")
        stock_query_manual_str = stock_query_manual + " " + image_location_str
        if stock_query_manual_str and submit:
            chat_result = trigger_code_executor_agent(stock_query_manual_str)
            st.image("code/" + image_name, use_column_width=True)
            st.write(chat_result)
    else:
        stock_query = st.selectbox(f'Select {option} stock query ?', stock_queries)
        if stock_query:
            submit = st.button("submit", type="primary")
            if image_name and submit:
                chat_result = trigger_code_executor_agent(stock_query)
                st.image("code/" + image_name, use_column_width=True)
                st.write(chat_result)

elif add_radio == "tools: market research":
    st.image("images/trade_vision_1.webp", width=300)
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

elif add_radio == "tools: stock predictions":
    st.image("images/task_weaver_2.png", use_column_width=True)
    st.write("Please visit the following link to access the stock price prediction tool")
    st.write("http://localhost:8000/")

elif add_radio == "tools: monte carlo simulation":
    initial_investment = st.text_input("Enter the initial investment amount :", 10000)
    num_simulations = st.text_input("Enter the number of simulations :", 1000)
    forecast_days = st.text_input("Enter the forecast days :", 365)
    desired_return = st.text_input("Enter the desired return :", 0.10)
    submit = st.button("submit", type="primary")
    if submit:
        var, conditional_var, probability_of_success = construct_simulation(ticker_map[option], int(initial_investment),
                                                                            int(num_simulations), int(forecast_days),
                                                                            float(desired_return))
        st.write(f"Value at Risk (95% confidence): £{var:,.2f}")
        st.write(f"Expected Tail Loss (Conditional VaR): £{conditional_var:,.2f}")
        desired_return_percent = desired_return * 100
        probability_of_success_percent = probability_of_success * 100
        st.write(
            f"Probability of achieving at least a {desired_return * 100}% return: {probability_of_success * 100:.2f}%")
        st.image('risk_simulation.png', use_column_width=True)

elif add_radio == "final report":
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
    st.markdown("To access the stock analyst tool , please visit the following link: [Stock Analyst :Crew AI]("
                "http://localhost:8003/)")

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
        col1, col2 = st.columns(2)
        with col1:
            st.write("stock highlights")
            st.write("highlights-from-knowledge-base")
            st.write("chat-with-knowledge-base")
            st.write("stock-performance: autogen")
        with col2:
            st.write("market-research: autogen")
            st.write("stock-price-prediction: taskweaver")
            st.write("buy-sell-hold: market_crew")
