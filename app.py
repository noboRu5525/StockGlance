import streamlit as st
import plotly.express as px
import pandas as pd
from home import home
from industry_analysis import industry_analysis

# streamlitの設定
st.set_page_config(
    layout='wide'
)

def main():
    page = st.sidebar.radio("Choose a page", ['ホーム', '業種', '業界（サンプル）'])
    if page == "ホーム":
        home()
    elif page == "業種":
        industry_analysis()
    elif page == "業界（サンプル）":
        # sample()
        pass


if __name__ == "__main__":
    main()