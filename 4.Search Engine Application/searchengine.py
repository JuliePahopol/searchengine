from flask import Flask, render_template, request
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

app = Flask(__name__, template_folder="./static/")


@app.route("/")
def websearch():
    return render_template("websearch.html")


@app.route("/a")
def a():
    return render_template("A.html")


@app.route("/b")
def b():
    return render_template("B.html")


@app.route("/c")
def c():
    return render_template("C.html")


@app.route("/d")
def d():
    return render_template("D.html")


@app.route("/e")
def e():
    return render_template("E.html")


@app.route("/websearch", methods=["GET", "POST"])
#Граф = сайты и связи между ними.
#PageRank = вычисление важности сайтов.
#Фильтрация = показываем только сайты с хорошим рейтингом.


def web_search():
    if request.method == "POST":
        query = request.form["query"]
        if query == "":
            return render_template("websearch.html")
        websites = [
            "http://localhost:5000/a",
            "http://localhost:5000/b",
            "http://localhost:5000/c",
            "http://localhost:5000/d",
            "http://localhost:5000/e",
        ]

        tokenized_text = load_tokenized_text("tokenized_text_pickle.pkl")
        tfidf = TfidfVectorizer()
        #Преобразование текста в числовые векторы с помощью TF-IDF
        # Вектор представляет собой набор чисел, которые показывают важность слов в тексте.
        tfidf_vectors = tfidf.fit_transform(
            [" ".join(tokens) for tokens in tokenized_text]
        )

        query_vector = tfidf.transform([query])

        similarities = cosine_similarity(query_vector, tfidf_vectors)
        # cosine similarity is to check the requests similarities in each doc (a,b,c,d,e)
        # Если два сайта похожи друг на друга (их схожесть больше 0),
        # мы создаем между ними связь. Например, если сайт A похож на сайт B,
        # то между ними появляется ребро с весом (схожестью).

        if all_zeros(similarities[0]):
            return render_template("notfound.html")

        G = nx.DiGraph()

        for i, link in enumerate(websites):
            G.add_node(link)
            for j, sim in enumerate(similarities[0]):
                if sim > 0 and i != j:
                    G.add_edge(link, websites[j], weight=sim)

        pagerank = nx.pagerank(G)
        #Результатом работы PageRank будет рейтинг каждого сайта.
        # Чем выше рейтинг, тем более важным считается сайт.


        ranked_results = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        #После вычисления важности, мы сортируем сайты по их рейтингу
        # от самого важного к менее важному.

        top_results = [x[0] for x in ranked_results if x[1] >= 0.14]
        #Мы отбираем только те сайты, которые имеют рейтинг 0.14 и выше.
        # Это помогает исключить сайты, которые не сильно связаны с запросом 
        # или не так важны

        return render_template("results.html", data=[top_results, query])


def load_tokenized_text(filename):
    tokenized_text = pickle.load(open(filename, "rb"))
    return tokenized_text


def all_zeros(l):
    for i in l:
        if i != 0:
            return False
    return True


if __name__ == "__main__":
    app.run(debug=True)
# adds new changes to the page without restarting the flask
