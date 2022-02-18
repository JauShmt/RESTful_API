import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sukurepa import db, create_app
from flask import Flask, Blueprint, request, jsonify
from .models import tablerinho
import json
import validators

scraper = Blueprint('scraper', __name__)



@scraper.route('/', methods=['GET'])
def hello_world():

    return 'This is my first API call!'



@scraper.route('/parser', methods=['POST'])
def home():

    try:
        url = request.json["url"]   #accept "url": as request body
        domain = "wikipedia.org"
        if domain in url:           #Check that URL belongs to wikipedia.org domain
            print(url)
            # Execute scrapping, parsing and commit it to the database
            return jsonify({
                "result": commit(parser(scrapeWikiArticle(url), url), url)
            })

        else:
            return jsonify("Only wikipedia links are allowed!")

    except KeyError:
        return jsonify("To parse a text send <<url>>: <<http://yoururl.com>> in the body of the request")


def scrapeWikiArticle(url):

    response = requests.get(url=url,)
    soup = BeautifulSoup(response.content, 'html.parser')
    # title = soup.find(id="firstHeading")
    article = soup.find('div', attrs={'class': 'mw-parser-output'}).text
    return article


def parser(article, url):

    split_list = article.split(" ")
    words = pd.value_counts(np.array(split_list))
    words = list(zip(words.index, words))
    json_result = words
    return json_result


def commit(json_result, url):

    if db.session.query(tablerinho.json_id).filter_by(json_urlerinho=url).first() is None:
        new_json = tablerinho(
            json_objecterinho = json_result,
            json_urlerinho = url
        )
        db.session.add(new_json)
        db.session.commit()
    query_response = tablerinho.query.with_entities(tablerinho.json_id).filter_by(json_urlerinho=url).first()
    return "Scrapping ok, parsing saved under ID:" + str(query_response[0])



@scraper.route('/list', methods=['GET'])
def get_url_from_db():

    query_result = tablerinho.query.with_entities(tablerinho.json_id, tablerinho.json_urlerinho,
                                                  tablerinho.json_annoterinho).distinct()
    url_list = [{"id": row.json_id, "url": row.json_urlerinho, "tag": row.json_annoterinho} for row in query_result]
    return jsonify(url_list)



@scraper.route('/tag', methods=['PATCH'])
def text_tagger():

    text_id = request.json["text_id"]
    tag = request.json["tag"]
    x = db.session.query(tablerinho).get(text_id)
    x.json_annoterinho = str(tag)
    db.session.commit()
    return "tag properly added to text n°" + str(text_id)



@scraper.route('/search', methods=['POST'])
def search():

    s_words = request.json["word"]
    text_query_r = tablerinho.query.with_entities(
        tablerinho.json_objecterinho,
        tablerinho.json_id,
        tablerinho.json_urlerinho
    )
    # print(text_query_r)
    result_list = []
    for row in text_query_r:
        # print(row)
        # print(type(row[0]))
        for word in row[0]:
            # print(type(word))
            # print(word)
            # print(word[0])
            # print(row[0])
            if word[0] == s_words:
                # print(type(word[0]))
                result_list.append({"text Id": row.json_id, "url": row.json_urlerinho, "with occurrences": word[1]})
    response = "Found <<" + s_words + ">> in: " + str(result_list)
    return jsonify(response)



@scraper.route('/delete', methods=['DELETE'])
def destroy():
    target_id = request.json["text_id"]
    db.session.query(tablerinho).filter(tablerinho.json_id == target_id).delete()
    db.session.commit()
    response = 'all your databases are belong to us'
    return response
