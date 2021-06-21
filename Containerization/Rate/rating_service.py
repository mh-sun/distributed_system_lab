from flask import Flask, request
from flask_mongoengine import MongoEngine

db = MongoEngine()

app = Flask(__name__)
db.init_app(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'Ratings',
    'host': 'mongodb-container',
    'port': 27017
}


class Rating(db.Document):
    rider = db.StringField()
    driver = db.StringField()
    rating = db.IntField()


def insert_into_database(rider, driver, rate):
    rate_info = Rating(rider=rider, driver=driver, rating=rate)
    rate_info.save()


@app.route("/rating", methods=["POST"])
def rating():
    data = request.json
    print("Connected")
    insert_into_database(data['rname'], data['dname'], data['rate'])
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
