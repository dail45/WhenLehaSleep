from flask import Flask
import datetime
import os
import requests

app = Flask(__name__)


@app.route('/when/')
def hello_world():
    now = datetime.datetime.now() + datetime.timedelta(hours=3)
    support = datetime.datetime.strptime("01:04:2021", "%d:%m:%Y")
    Y, m, d, H, M = now.strftime("%Y:%m:%d:%H:%M").split(":")
    deltadt = now - support
    delta = int(deltadt.days) % 4 + 1
    timeit = f"{H}:{M} {d}:{m}:{Y}"
    H = int(H)
    if delta == 1:
        if 8 <= H < 20:
            status = "Лёха на дневной.\n" + timeit + "\nstatus = Дневной"
        elif H < 8:
            status = "Лёха спит.\n" + timeit + "\nstatus = Дневной"
        elif 20 <= H < 21:
            status = "Лёха спешит домой.\n" + timeit + "\nstatus = Дневной"
        elif H >= 21:
            status = "Лёха дома.\n" + timeit + "\nstatus = Дневной"
    elif delta == 2:
        if H < 19:
            status = "Лёха дома.\n" + timeit + "\nstatus = Ночная"
        if H >= 19:
            status = "Лёха на ночной.\n" + timeit + "\nstatus = Ночная"
    elif delta == 3:
        if H <= 8:
            status = "Лёха на ночной.\n" + timeit + "\nstatus = Отсыпной"
        elif H > 8:
            status = "Лёха спит(дома).\n" + timeit + "\nstatus = Отсыпной"
    elif delta == 4:
        status = "Лёха дома.\n" + timeit + "\nstatus = Выходной"
    return status


@app.route('/url/<URL>')
def image_return(URL):
    return requests.get(URL)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


