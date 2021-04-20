import flask
from flask import Flask, request
import socketio

app = Flask(__name__)
sio = socketio.Server()
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


@app.route("/comm", methods=["GET", "POST"])
def send_pair():
    info = request.json
    print("message received from ride :", info)
    sio.emit("notify", info)
    return flask.Response(status=201)
