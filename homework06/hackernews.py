from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    redirect("/news")


@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE


if __name__ == "__main__":
    run(host="localhost", port=8080)

