import streamlit as st
import plotly.express as px
import pandas as pd

# サンプルデータセットを読み込む
df = px.data.iris()

# Plotlyで散布図を描画する
fig_scatter = px.scatter(df, x="sepal_width", y="sepal_length")
selection = st.plotly_chart(fig_scatter, key="iris_scatter", on_select="rerun")

# selectionには選択されたデータが入っている
with st.expander("selection"):
    st.write(selection)

# selectionをDataFrameに変換してから表示する
df_selected = pd.DataFrame(selection["selection"]["points"])
st.dataframe(df_selected)
