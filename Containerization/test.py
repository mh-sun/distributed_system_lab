import requests
from socketIO_client import SocketIO, LoggingNamespace
import socketio

socket = socketio.Client()
socket.connect('http://127.0.0.1:8003', namespaces=['/confirmation'])


@socket.event(namespace='/confirmation')
def message(data):
    print(data)


data = "Hello from client"
requests.post("http://127.0.0.1:8003/comm", json=data)
