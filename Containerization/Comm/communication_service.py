import flask
from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)


@app.route("/comm", methods=["GET", "POST"])
def send_pair():
    info = request.json
    print("message received from ride :", info)
    sio.emit("notify", info)
    return flask.Response(status=201)


if __name__ == '__main__':
    sio.run(app, port=8003)
