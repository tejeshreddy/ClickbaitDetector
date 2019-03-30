from flask import Flask, request, abort
import requests
from readability import Document
import json
from subprocess import check_output

from utils.get_news import get_news_from_headlines

app = Flask(__name__)


@app.route("/", methods=["POST"])
def main_page():
    """
        - Handles incoming request from extension.
        - Retrieves URL from JSON and gets HTML content of page.
        - Cleans up HTML using Python Readability.
        - Sends headlines and summary to model.
    """
    url = request.get_json()["url"]

    page_content = requests.get(url).text

    cleaned_page_content = Document(page_content)
    headline = cleaned_page_content.title()

    percentage = run_model(headline)

    response = app.response_class(
        response=json.dumps({"url": url, "headline": headline, "percentage": percentage}),
        status=200,
        mimetype="application/json"
    )
    return response


def run_model(headline):
    """
        - Run trained model on new article.
        - Passes headlines and summary to model.
    """
    # TODO: Call model with headlines.
    val = check_output("python source\predict.py \"{}\"".format(headline))
    return float(val.decode("utf8").replace("\r\n", ""))
    # compare_similar_news(headlines)
    pass


def compare_similar_news(headlines):
    """
        - Calls utility function to get similar articles from Google News.
        - Compares news to check how similar the articles are.
        - Only used if clickabit detected percentage is low.
    """
    similar_articles = get_news_from_headlines(headlines)
    # TODO: Compare articles
    pass


if __name__ == "__main__":
    app.run(port=5000, debug=True)
