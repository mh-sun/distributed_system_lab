import requests
from socketIO_client import SocketIO, LoggingNamespace
import socketio




data = {
    'rname':'mehedi',
    'dname':'sun',
    'rate':20
}
requests.post("http://127.0.0.1:8000/rate", json=data)
