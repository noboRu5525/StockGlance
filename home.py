import streamlit as st
import pandas as pd

# EDINETコード表
edinetcode = pd.read_csv('./data/Edinetcode.csv', header=1, encoding='cp932')
print(edinetcode)

def home(): 
    st.title('ホーム')
    st.write(edinetcode.columns)


    # テキスト入力ボックス
    text_input = st.text_input('検索するEDINETコードまたは提出者名の一部を入力してください', '')

    # 入力がある場合にフィルタリングを実行
    if text_input:
        # EDINETコードまたは提出者名にキーワードが含まれる行を抽出
        filtered_data = edinetcode[
            edinetcode['ＥＤＩＮＥＴコード'].astype(str).str.contains(text_input, case=False, na=False) |
            edinetcode['提出者名'].str.contains(text_input, case=False, na=False)
        ]
    else:
        # 入力がない場合は全データを表示
        filtered_data = edinetcode

    # DataFrameをテーブル形式で表示
    st.dataframe(filtered_data)

# 実行
if __name__ == '__main__':
    home()
