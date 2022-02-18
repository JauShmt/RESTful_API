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


# api = Api(app)
# url_post_args = reqparse.RequestParser()
# url_post_args.add_argument("url", type=str, help="wikipedia link")
# url={}


@scraper.route('/', methods=['GET'])
def hello_world():
    return 'This is my first API call!'


@scraper.route('/parser', methods=['POST'])
def home():
    # global url
    # url = "https://en.wikipedia.org/wiki/Web_scraping"
    url = request.json["url"]
    print(url)
    return jsonify({
        "result": parser(scrapeWikiArticle(url), url)
    })
    # return parser(scrapeWikiArticle(url),url)


def parser(x, url):
    split_list = x.split(" ")
    # print(type(split_list))
    words = pd.value_counts(np.array(split_list))
    # print(words)
    # print(type(words))
    words = list(zip(words.index, words))
    words = words
    print(words[0])
    # print(type(words[0]))
    print(words)
    # print(type(words))
    json_result = words
    print(json_result)
    if db.session.query(tablerinho.json_id).filter_by(json_urlerinho=url).first() is None:
        new_json = tablerinho(
            json_objecterinho=json_result,
            json_urlerinho=url
        )
        db.session.add(new_json)
        db.session.commit()
    query_response = tablerinho.query.with_entities(tablerinho.json_id).filter_by(json_urlerinho=url).first()
    return "Scrapping ok, parsing saved under ID:" + str(query_response[0])


def scrapeWikiArticle(url):
    response = requests.get(
        url=url,
    )

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")
    # print(title.text)
    p1 = soup.find('div', attrs={'class': 'mw-parser-output'}).text
    # print(type(p1))
    return p1


@scraper.route('/list', methods=['GET'])
def get_url_from_db():
    query_result = tablerinho.query.with_entities(tablerinho.json_id, tablerinho.json_urlerinho, tablerinho.json_annoterinho).distinct()
    url_list = [{"id": row.json_id, "url": row.json_urlerinho, "tag": row.json_annoterinho} for row in query_result]
    # print(url_list)
    # url_list = tuple(zip(url_list))
    # print(url_list)
    # id_query = tablerino.query.with_entities(tablerino.json_id).distinct()
    # id_list = [id[0] for id in id_query]
    # response = [url_list] + [id_list]
    # json_result = json.dumps(response, ensure_ascii=False)
    # print(json_result)
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
    text_query_r = tablerinho.query.with_entities(tablerinho.json_objecterinho,tablerinho.json_id, tablerinho.json_urlerinho)
    # print(text_query_r)
    result_list=[]
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
                occurences = word[1]
    response = "Found <<"+s_words+">> in: " + str(result_list)
    return jsonify(response)




@scraper.route('/delete', methods=['DELETE'])
def destroy():
    target_id = request.json["text_id"]
    db.session.query(tablerinho).filter(tablerinho.json_id == target_id).delete()
    db.session.commit()
    response = 'all your databases are belong to us'
    return response

# def bn_tree():
# children = sorted(words, key=lambda x: x[1])
# parent = children.pop()[0]
# G = nx.balanced_tree(2, 5)
# # for word, occurence in children: G.add_edge(parent, word, weight=occurence)
# # width = list(nx.get_edge_attributes(G, 'weight').values())
# nx.draw_networkx(G)
# plt.show()
# print(nx.is_tree(G))


# test= parser(scrapeWikiArticle(url))
# print('test ok')

# def get_json_tree(url_to_scrape):
#     result = full_page_word_counts(url_to_scrape)
#     sorted_r = dict(sorted(result.items(), key=operator.itemgetter(1),reverse=True))
#     json_result = json.dumps(sorted_r, ensure_ascii=False)
#     json_to_database(json_result, url_to_scrape)
#
# def json_to_database(json_result, url_to_scrape):
#     if db.session.query(tablerino.json_id).filter_by(json_urlerino=url_to_scrape).first() is None:
#         new_json = tablerino(
#             json_objecterino = json_result,
#             json_urlerino = url_to_scrape
#         )
#         db.session.add(new_json)
#         db.session.commit()
#
#         flash("C'EST DANS LA BASE! T'ES VRAIMENT TROP FORT! ᕕ( ᐛ )ᕗ", category='success')
#     else:
#         flash ("POURQUOI TU AJOUTES DEUX FOIS LA MÊME PAGE?! T'ES CON OU QUOI?! (‡▼益▼)", category='error')
#     return render_template('homepage.html')
