import nltk
from newspaper import Article

nltk.download("punkt_tab")

url = "https://denev6.tistory.com/entry/til-3"

article = Article(url, language="ko")
article.download()
article.parse()

# 출력
# print(article.title)
# print(article.text)
# print(article.top_image)
# article.nlp()
# print(article.summary)

with open("doc.txt", "w", encoding="utf-8") as f:
    f.write(article.text)
