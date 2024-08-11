import streamlit as st
import stock_screener as sm
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import prompt_template as pt
from tickers_list import tickers_list
import time
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv('google_api_key')

st.set_page_config(page_title= "Stock Analyzer",layout="wide")
col1, col2 = st.columns(2)

generation_config = {
  "temperature": 0,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

if "chat_llm" not in st.session_state:
    st.session_state.chat_llm = chat_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=google_api_key,generation_config=generation_config)

if "funda_data" not in st.session_state:
    st.session_state.funda_data = None

if "sector_data" not in st.session_state:
    st.session_state.sector_data = None

if "scraper" not in st.session_state:
    st.session_state.scraper  = sm.StockScreenerScraper()

if "chains" not in st.session_state:
    st.session_state.chains  = [ChatPromptTemplate.from_template(template=pt.stats_template) | st.session_state.chat_llm, ChatPromptTemplate.from_template(template=pt.sector_template) | st.session_state.chat_llm]

with col1:
    st.header("AI Stock Analyzer")
    st.image("logo.png",width=400)
    option = st.selectbox(
    "Select a Stock:",
    tickers_list,
)
    if st.button('Analyze',type='primary'):
        st.session_state.funda_data, st.session_state.sector_data = st.session_state.scraper.get_full_data(option)

        with col1:
            with st.spinner('Wait for it...'):
                stat_res = st.session_state.chains[0].invoke({"text": st.session_state.funda_data}).content
                st.markdown(stat_res)

        with col2:
            with st.spinner('Wait for it...'):
                time.sleep(5)
                pl_res = st.session_state.chains[1].invoke({"text": st.session_state.sector_data}).content
                st.markdown(pl_res)