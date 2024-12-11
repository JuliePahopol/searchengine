from flask import Flask, render_template, request
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import json
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from pathlib import Path


app = Flask(__name__, template_folder="./static/")


@app.route("/")
def websearch():
    return render_template("websearch.html")


@app.route("/imagesearch")
def imagesearch():
    return render_template("imagesearch.html")


@app.route("/reverseimagesearch")
def reverseimagesearch():
    return render_template("reverseimagesearch.html")


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
# Граф = сайты и связи между ними.
# PageRank = вычисление важности сайтов.
# Фильтрация = показываем только сайты с хорошим рейтингом.


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
        # Преобразование текста в числовые векторы с помощью TF-IDF
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
        # Результатом работы PageRank будет рейтинг каждого сайта.
        # Чем выше рейтинг, тем более важным считается сайт.

        ranked_results = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        # После вычисления важности, мы сортируем сайты по их рейтингу
        # от самого важного к менее важному.

        top_results = [x[0] for x in ranked_results if x[1] >= 0.14]
        # Мы отбираем только те сайты, которые имеют рейтинг 0.14 и выше.
        # Это помогает исключить сайты, которые не сильно связаны с запросом
        # или не так важны

        return render_template("results.html", data=[top_results, query])


@app.route("/search_images", methods=["GET", "POST"])
def search_images():
    if request.method == "POST":
        query = request.form["query"].lower()

        if query == "":
            return render_template("imagesearch.html")

        with open("images.json", "r") as f:
            images = json.load(f)

        # search for img with alt text and the title that contain the query term
        results = []
        for img in images:
            if query in img["alt_text"] or query in img["title"]:
                results.append(img)

            else:
                continue

        if len(results) == 0:
            return render_template("notfound.html")

        return render_template("imageresults.html", data=[results, query])


fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/reverse_img_store") / (feature_path.stem + ".jpg"))


features = np.array(features)
if features.shape[0] == 0:
    raise ValueError("The features array is empty. No features found.")
else:
    print(f"Loaded {features.shape[0]} features.")


@app.route("/reverseimagesearchresult", methods=["GET", "POST"])
def reverseimagesearchresult():

    if request.method == "POST":
        file = request.files["query_img"]

        # save query img
        img = Image.open(file.stream)  # PIL img
        uploaded_img_path = (
            "./static/uploaded/"
            + datetime.now().isoformat().replace(":", ".")
            + "_"
            + file.filename
        )

        img.save(uploaded_img_path)

        # run the search
        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)
        ids = np.argsort(dists)[:3]
        scores = [(dists[id], img_paths[id]) for id in ids]

        return render_template(
            "reverseimagesearch.html", query_path=uploaded_img_path, scores=scores
        )
    else:
        return render_template("reverseimagesearch.html")


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
