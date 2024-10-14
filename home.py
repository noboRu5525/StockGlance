import streamlit as st
import pandas as pd
import os
import re
import plotly.express as px

# EDINETコード表
edinetcode = pd.read_csv('./data/Edinetcode.csv', header=1, encoding='cp932')

def home():
    st.title('リアルタイム検索機能付き EDINET コード検索システム')

    # テキスト入力ボックス（リアルタイムに検索）
    text_input = st.text_input('検索するEDINETコードまたは提出者名の一部を入力してください', '')

    # 入力がある場合にリアルタイムにフィルタリングを実行
    if text_input:
        # 正規表現を使って曖昧検索を実行（部分一致、大文字小文字を区別しない）
        # 文字列のどこかに `text_input` が含まれていればヒットさせる
        filtered_data = edinetcode[
            edinetcode['ＥＤＩＮＥＴコード'].astype(str).str.contains(re.escape(text_input), case=False, na=False) |
            edinetcode['提出者名'].str.contains(re.escape(text_input), case=False, na=False)
        ]
    else:
        # 入力がない場合は全データを表示
        filtered_data = edinetcode

    # フィルタリングされたDataFrameをリアルタイムにテーブル形式で表示
    st.dataframe(filtered_data)

    # フィルタリングされたデータから会社を選択するセレクトボックスを作成
    if not filtered_data.empty:
        selected_company = st.selectbox(
            '詳細データを表示する会社を選んでください',
            filtered_data['ＥＤＩＮＥＴコード']
        )

        # 特定の会社が選択された場合、詳細データを読み込んで可視化
        if selected_company:
            # 選択されたEDINETコードに対応する証券コードを取得
            edinet_code = filtered_data[filtered_data['ＥＤＩＮＥＴコード'] == selected_company]['ＥＤＩＮＥＴコード'].values[0]
            security_code = filtered_data[filtered_data['ＥＤＩＮＥＴコード'] == selected_company]['証券コード'].values[0]
            visualize_company_data(edinet_code, security_code)

def visualize_company_data(edinet_code, security_code):
    # 対応するファイル名を構築
    file_path = f'./data/AnnualSecuritiesReport/{edinet_code}_{security_code}.csv'

    # ファイルが存在する場合のみ読み込み
    if os.path.exists(file_path):
        company_data = pd.read_csv(file_path, index_col=0, encoding='utf-8')

        # データの可視化例
        st.subheader(f'証券コード: {security_code} の詳細データ')
        st.write(company_data)

        # グラフを横2列に表示するための列を作成
        col1, col2 = st.columns(2)

        # カスタムプロットを作成する関数
        def plot_bar_chart(column_name, col, positive_color):
            if column_name in company_data.columns:
                df = company_data[[column_name]].reset_index()
                df.columns = ['Year', column_name]  # プロットのために列名をリセット

                # プラスとマイナスの値で色を分けてプロット
                fig = px.bar(
                    df,
                    x='Year',
                    y=column_name,
                    color=df[column_name].apply(lambda x: 'positive' if x >= 0 else 'negative'),
                    color_discrete_map={'positive': positive_color, 'negative': 'red'},
                    title=column_name
                )
                col.plotly_chart(fig)

        # グラフを表示、各グラフに異なる色を設定
        plot_bar_chart('売上高、経営指標等', col1, 'blue')
        plot_bar_chart('経常利益又は経常損失（△）', col2, 'green')
        plot_bar_chart('資産', col1, 'orange')
        plot_bar_chart('現金及び預金', col2, 'purple')
        plot_bar_chart('利益剰余金', col1, 'blue')
        plot_bar_chart('当期純利益又は当期純損失（△）、経営指標等', col2, 'green')
        plot_bar_chart('営業活動によるキャッシュ・フロー', col1, 'orange')
        plot_bar_chart('従業員数', col2, 'purple')

    else:
        st.warning(f'データファイルが見つかりません: {file_path}')

# 実行
if __name__ == '__main__':
    home()
