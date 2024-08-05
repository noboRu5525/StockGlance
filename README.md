任意ディレクトリにて以下のコードを順番に実行する

```jsx
git clone https://github.com/noboRu5525/streamlit_base.git
```

```jsx
cd streamlit_base
```

ビルド

```jsx
docker build -t streamlit_app .
```

実行

```jsx
docker run --rm -p 8501:8501 streamlit_app
```

基本的にapp.pyを変更する．

追加したいライブラリに関してはrequirements.txtに追加する．

app.pyを変更したらビルド→実行の手順を踏む．
