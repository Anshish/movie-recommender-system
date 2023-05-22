from flask import Flask
import pandas as pd
from pymongo import MongoClient, InsertOne
import certifi

app = Flask(__name__)

ca = certifi.where()

# 1. Import movies dataset
movies = pd.read_pickle('./datasets/movies.pkl')

# 2. Create MongoDB client
url = 'mongodb+srv://admin-anshish:test123@cluster0.2gzry.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile=certifi.where())
db = client['movie_database']
ratings = db['ratings']

bulk_operations = []

for index, row in movies.iterrows():
    movie_data = {
        "movie_id": int(row["id"]),
        "movie_name": row["title"],
        "vote_average": float(row["vote_average"]),
        "vote_count": int(row["vote_count"]),
    }
    bulk_operations.append(InsertOne(movie_data))

if bulk_operations:
    ratings.bulk_write(bulk_operations)

client.close()
