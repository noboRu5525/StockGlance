任意ディレクトリにて以下のコードを順番に実行する

```jsx
git clone https://github.com/noboRu5525/StockGlance.git
```

```jsx
cd StockGlance
```

ビルド

```jsx
docker build -t stockglance .
```

実行

```jsx
docker run -p 8501:8501 -v $(pwd):/app --rm -it stockglance
```

基本的にapp.pyを変更する．

追加したいライブラリに関してはrequirements.txtに追加する．

app.pyを変更したらビルド→実行の手順を踏む．
