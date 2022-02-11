from flask import Flask
import datetime
import os
import requests

app = Flask(__name__)
support = datetime.datetime.strptime("01:04:2021", "%d:%m:%Y")

# @app.route('/')
def hello_world(d, m, Y, H, M, now):
    status = ""
    Y, m, d, H, M = now.strftime("%Y:%m:%d:%H:%M").split(":")
    deltadt = now - support
    delta = int(deltadt.days) % 4 + 1
    timeit = f"{H}:{M} {d}:{m}:{Y}"
    H = int(H)
    if delta == 1:
        if 8 <= H < 20:
            status = "Лёха на дневной.<br>"
        elif H < 8:
            status = "Лёха спит.<br>"
        elif 20 <= H < 21:
            status = "Лёха спешит домой.<br>"
        elif H >= 21:
            status = "Лёха дома.<br>"
        status += timeit + "<br>status = Дневной &#x1F506"
    elif delta == 2:
        if H < 19:
            status = "Лёха дома.<br>"
        if H >= 19:
            status = "Лёха на ночной.<br>"
        status += timeit + "<br>status = Ночная &#127769"
    elif delta == 3:
        if H <= 8:
            status = "Лёха на ночной.<br>"
        elif H > 8:
            status = "Лёха спит(дома).<br>"
        status += timeit + "<br>status = Отсыпной &#128719"
    elif delta == 4:
        status = "Лёха дома.<br>" + timeit + "<br>status = Выходной &#128994"
    return f"""
<html>
<head>
    <title>WhenLehaSleep</title>
</head>
<body>
<h1 align="Center">
    {status}
</h1>
</body>
</html>"""

@app.route('/<str:data>')
def hello_world2(data):
    status = ""
    now = datetime.datetime.now() + datetime.timedelta(hours=3)
    d, m, Y, H, M = now.strftime("%d:%m:%Y:%H:%M").split(":")
    if not data:
        return hello_world(d, m, Y, H, M, now)
    elif data.count(":") == 0:
        d = data
        now = now.strptime(f"{d}:{m}:{Y}:{H}:{M}", "%d:%m:%Y:%H:%M")
        return hello_world(d, m, Y, H, M, now)
    elif data.count(":") == 1:
        d, m = data.split(":")
        now = now.strptime(f"{d}:{m}:{Y}:{H}:{M}", "%d:%m:%Y:%H:%M")
        return hello_world(d, m, Y, H, M, now)
    elif data.count(":") == 2:
        d, m, Y = data.split(":")
        now = now.strptime(f"{d}:{m}:{Y}:{H}:{M}", "%d:%m:%Y:%H:%M")
        return hello_world(d, m, Y, H, M, now)
    else:
        return hello_world(d, m, Y, H, M, now)


if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except Exception as f:
        print(f)
