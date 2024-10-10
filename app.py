import streamlit as st
import plotly.express as px
import pandas as pd
from home import home

def main():
    page = st.sidebar.radio("Choose a page", ['ホーム', '検索（サンプル）', '業界（サンプル）'])
    if page == "ホーム":
        home()
    elif page == "検索（サンプル）":
        # sample()
        pass
    elif page == "業界（サンプル）":
        # sample()
        pass


if __name__ == "__main__":
    main()