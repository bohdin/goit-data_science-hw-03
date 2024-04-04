from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

client = MongoClient("mongodb+srv://goitlearn:1234@cluster0.pwocrpk.mongodb.net/", server_api=ServerApi("1"))

qoutes = client.book.qoutes
with open("qoutes.json", 'r') as f:
    data = json.load(f)
    qoutes.insert_many(data)

authors = client.book.authors
with open('authors.json', 'r') as f:
    data = json.load(f)
    authors.insert_many(data)