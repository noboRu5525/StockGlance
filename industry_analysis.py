import streamlit as st
import pandas as pd
import re
import os
import plotly.express as px


# EDINETコード表
edinetcode = pd.read_csv('./data/Edinetcode.csv', header=1, encoding='cp932')

# グラフ表示の関数
def plot_bar_chart(column_name, col, color, company_data):
    if column_name in company_data.columns:
        df = company_data[[column_name]].reset_index()
        df.columns = ['年度', column_name]  # プロット用にカラムを整える
        fig = px.bar(df, x='年度', y=column_name, color_discrete_sequence=[color], title=column_name)
        col.plotly_chart(fig)

# グラフ表示の関数（箱ひげ図用）
def plot_box_chart(column_name, col, company_data):
    if column_name in company_data.columns:
        df = company_data[[column_name]].reset_index()
        df.columns = ['年度', column_name]  # プロット用にカラムを整える
        fig = px.box(df, x='年度', y=column_name, title=column_name)
        col.plotly_chart(fig)

def industry_analysis():
    st.title('業種別分析')

    # 業界を選択するセレクトボックス
    industry = st.selectbox('業界を選んでください', edinetcode['提出者業種'].unique())

    # 選択された業界に属する会社をフィルタリング
    filtered_data = edinetcode[edinetcode['提出者業種'] == industry]

    # フィルタリングされた業界別データを表示
    st.write(f'{industry} 業種のデータ:')
    st.dataframe(filtered_data)

    # 業界別に簡単な分析（例として、会社数を表示）
    company_count = filtered_data['提出者名'].count()
    st.write(f'{industry} 業種の会社数: {company_count}社')

    # 業界ごとの売上や利益などの年度別平均を表示
    col1, col2 = st.columns(2)

    if not filtered_data.empty:
        # 業界内の会社ごとのデータを収集
        yearly_data = []

        for index, row in filtered_data.iterrows():
            edinet_code = row['ＥＤＩＮＥＴコード']
            security_code = row['証券コード']
            file_path = f'./data/AnnualSecuritiesReport/{edinet_code}_{security_code}.csv'
            if os.path.exists(file_path):
                company_data = pd.read_csv(file_path, index_col=0, encoding='utf-8')
                yearly_data.append(company_data)

        # 年度ごとの平均を計算
        if yearly_data:
            combined_data = pd.concat(yearly_data)
            # 数値データのみを抽出
            numeric_data = combined_data.select_dtypes(include=['float64', 'int64'])


            # 箱ひげ図に変更
            plot_box_chart('売上高、経営指標等', col1, numeric_data)
            plot_box_chart('経常利益又は経常損失（△）', col2, numeric_data)
            plot_box_chart('資産', col1, numeric_data)
            plot_box_chart('現金及び預金', col2, numeric_data)
            plot_box_chart('利益剰余金', col1, numeric_data)
            plot_box_chart('当期純利益又は当期純損失（△）、経営指標等', col2, numeric_data)
            plot_box_chart('営業活動によるキャッシュ・フロー', col1, numeric_data)
            
            # 数値データに対して年度ごとの平均を計算
            # combined_data_mean = numeric_data.groupby(numeric_data.index).mean()

            # plot_bar_chart('売上高、経営指標等', col1, 'blue', combined_data_mean)
            # plot_bar_chart('経常利益又は経常損失（△）', col2, 'green', combined_data_mean)
            # plot_bar_chart('資産', col1, 'orange', combined_data_mean)
            # plot_bar_chart('現金及び預金', col2, 'purple', combined_data_mean)
            # plot_bar_chart('利益剰余金', col1, 'brown', combined_data_mean)
            # plot_bar_chart('当期純利益又は当期純損失（△）、経営指標等', col2, 'pink', combined_data_mean)
            # plot_bar_chart('営業活動によるキャッシュ・フロー', col1, 'cyan', combined_data_mean)
        else:
            st.write('データが見つかりませんでした')

# 実行
if __name__ == '__main__':
    industry_analysis()