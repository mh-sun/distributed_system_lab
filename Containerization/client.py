import requests
import random
import time
import socketio

sio = socketio.Client()
sio.connect("http://127.0.0.1:8003")


def get_location():
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    temp = [a, b]

    return temp


def get_rider():
    size = len(riders)
    if size > 0:
        num = random.randint(0, size - 1)
        global busy_riders
        rid = riders.pop(num)
        busy_riders.append(rid)
        return rid


def get_driver():
    size = len(drivers)
    if size > 0:
        num = random.randint(0, size - 1)
        global busy_drivers
        driv = drivers.pop(num)
        busy_drivers.append(driv)
        return driv


def store_rider(name):
    riders.append(name)
    if name in busy_riders:
        busy_riders.remove(name)


def store_driver(name):
    for driv in busy_drivers:
        if driv[0] == name:
            index = busy_drivers.index(driv)
            drivers.append(busy_drivers.pop(index))
            return


def send_rating(r_name, d_name):
    rate = random.randint(1, 5)
    rate_req = {
        "rname": r_name,
        "dname": d_name,
        "rate": rate
    }
    requests.post("http://127.0.0.1:8005/rating", json=rate_req)


@sio.event()
def notify(data):
    store_rider(data['r_name'])
    store_driver(data['d_name'])
    print("%s Have to give %s %d TAKA " %
          (data['r_name'], data['d_name'], data['fare']))
    send_rating(data['r_name'], data['d_name'])


riders = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"]

drivers = [["d1", "car1"], ["d2", "car2"], [
    "d3", "car3"], ["d4", "car4"], ["d5", "car5"], ["d6", "car6"], ["d7", "car7"], ["d8", "car8"], ["d9", "car9"],
           ["d10", "car10"]]

busy_drivers = []
busy_riders = []

while True:
    r = get_rider()
    d = get_driver()

    if not r or not d:
        continue

    print("%s wants to ride" % r)
    print("%s wants to drive" % d[0])

    rider_req = {
        "name": r,
        "loc": get_location(),
        "des": get_location()
    }

    driver_req = {
        "name": d[0],
        "car": d[1],
        "loc": get_location()
    }

    requests.post("http://127.0.0.1:8005/api/rider", json=rider_req)
    requests.post("http://127.0.0.1:8005/api/driver", json=driver_req)

    time.sleep(2)
