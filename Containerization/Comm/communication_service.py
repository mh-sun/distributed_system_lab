from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
sio = SocketIO(app)


@app.route("/comm", methods=["POST"])
def send_pair():
    info = request.json
    print("message received from ride :", info)
    sio.emit("notify", info)
    return "Communication received from ride share"


if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=8080)
