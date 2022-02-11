from flask import Flask
import datetime
import os
import requests

app = Flask(__name__)


@app.route('/')
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
            status = "Лёха на дневной.<br>" + timeit + "<br>status = Дневной &#9728"
        elif H < 8:
            status = "Лёха спит.<br>" + timeit + "<br>status = Дневной &#9728"
        elif 20 <= H < 21:
            status = "Лёха спешит домой.<br>" + timeit + "<br>status = Дневной &#9728"
        elif H >= 21:
            status = "Лёха дома.<br>" + timeit + "<br>status = Дневной &#9728"
    elif delta == 2:
        if H < 19:
            status = "Лёха дома.<br>" + timeit + "<br>status = Ночная"
        if H >= 19:
            status = "Лёха на ночной.<br>" + timeit + "<br>status = Ночная"
    elif delta == 3:
        if H <= 8:
            status = "Лёха на ночной.<br>" + timeit + "<br>status = Отсыпной"
        elif H > 8:
            status = "Лёха спит(дома).<br>" + timeit + "<br>status = Отсыпной"
    elif delta == 4:
        status = "Лёха дома.<br>" + timeit + "<br>status = Выходной"
    return f"""<html>
<head>
    <title>WhenLehaSleep</title>
</head>
<body>
<h1 align="Center">
    {status}
</h1>
</body>
</html>"""


if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except Exception as f:
        print(f)
