from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

# Підключення до MongoDB
client = MongoClient("mongodb+srv://goitlearn:1234@cluster0.pwocrpk.mongodb.net/", server_api=ServerApi("1"))

# Вибір колекції 'qoutes' у базі даних 'book'
qoutes = client.book.qoutes
with open("qoutes.json", 'r') as f:
    # Завантаження даних з файлу у форматі JSON
    data = json.load(f)
    # Вставка завантажених даних у вибрану колекцію
    qoutes.insert_many(data)

# Вибір колекції 'authors' у базі даних 'book'
authors = client.book.authors
with open('authors.json', 'r') as f:
    # Завантаження даних з файлу у форматі JSON
    data = json.load(f)
    # Вставка завантажених даних у вибрану колекцію
    authors.insert_many(data)
    