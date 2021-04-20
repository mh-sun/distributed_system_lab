import requests
import socketio
import random
import time
import json

sio = socketio.Client()
sio.connect("http://127.0.0.1:8003/")


class rider:
    def __init__(self, name, loc, des):
        self.name = name
        self.loc = loc
        self.des = des


class driver:
    def __init__(self, driv, loc):
        self.name = driv[0]
        self.car = driv[1]
        self.loc = loc


def get_location():
    a = random.randint(0, 100)
    b = random.randint(0, 100)

    return [a, b]


def get_rider():
    size = len(riders)
    if size > 0:
        num = random.randint(0, size - 1)
        rid = riders.pop(num)
        return rid


def store_rider(name):
    riders.append(name)


def get_driver():
    size = len(drivers)
    if size > 0:
        num = random.randint(0, size - 1)
        global busy_drivers
        driv = drivers.pop(num)
        busy_drivers.append(driv)
        return driv


def store_driver(name):
    for driv in busy_drivers:
        if driv[0] == name:
            index = busy_drivers.index(driv)
            drivers.append(busy_drivers.pop(index))
            return


def send_rating(r_name, d_name):
    rate = random.randint(1, 5)
    rate_req = json.dumps({"rname": r_name, "dname": d_name, "rate": rate})
    requests.post("http://127.0.0.1:8000/rate", json=rate_req)


@sio.event
def notify(data):
    store_rider(data['r_name'])
    store_driver(data['d_name'])
    print("%s Have to give %s %d TAKA " % (data['r_name'], data['d_name'], data['fare']))
    send_rating(data['r_name'], data['d_name'])


riders = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"]

drivers = [["d1", "car1"], ["d2", "car2"], [
    "d3", "car3"], ["d4", "car4"], ["d5", "car5"], ["d6", "car6"], ["d7", "car7"], ["d8", "car8"], ["d9", "car9"],
           ["d10", "car10"]]

busy_drivers = []

while True:
    r = get_rider()
    d = get_driver()

    if not r or not d:
        continue

    print("%s wants to ride" % r)
    print("%s wants to drive" % d[0])

    rider_req = json.dumps(rider(r, get_location(), get_location()).__dict__)
    driver_req = json.dumps(driver(d, get_location()).__dict__)

    requests.post("http://127.0.0.1:8000/api/rider", json=rider_req)
    requests.post("http://127.0.0.1:8000/api/driver", json=driver_req)

    time.sleep(3)

