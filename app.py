from flask import Flask
import datetime
import os
import requests


def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i + 2], 16) for i in range(1, 6, 2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#" + "".join(["0{0:x}".format(v) if v < 16 else
                          "{0:x}".format(v) for v in RGB])


def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
      colors in RGB and hex form for use in a graphing function
      defined later on '''
    return {"hex": [RGB_to_hex(RGB) for RGB in gradient],
            "r": [RGB[0] for RGB in gradient],
            "g": [RGB[1] for RGB in gradient],
            "b": [RGB[2] for RGB in gradient]}


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
      two hex colors. start_hex and finish_hex
      should be the full six-digit color string,
      inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n-1):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)
    RGB_list.append(f)
    return color_dict(RGB_list)


app = Flask(__name__)
support = datetime.datetime.strptime("01:04:2021", "%d:%m:%Y")
mouthsTimes = {1: "08:06 08:50 16:27 17:11",
               2: "07:18 07:56 17:31 18:10",
               3: "06:11 06:47 18:30 19:07",
               4: "04:47 05:27 19:33 20:13",
               5: "03:31 04:20 20:32 21:22",
               6: "02:43 03:44 21:15 22:16",
               7: "03:08 04:04 21:05 22:00",
               8: "04:15 04:58 20:08 20:51",
               9: "05:21 05:58 18:50 19:27",
               10: "06:20 06:57 17:32 18:09",
               11: "07:20 08:02 16:24 17:06",
               12: "08:05 08:51 15:56 16:42"}
Colors = {"startUp": "#730000",
          "endUp": "#ff7300",
          "startDown": "#ff7300",
          "endDown": "#730000",
          "dayMiddle": "#ffff00",
          "nightMiddle": "000000"}
dayStatus = {0: [Colors["nightMiddle"], Colors["startUp"]],
             1: [Colors["startUp"], Colors["endUp"]],
             2: [Colors["endUp"], Colors["dayMiddle"]],
             3: [Colors["dayMiddle"], Colors["startDown"]],
             4: [Colors["startDown"], Colors["endDown"]],
             5: [Colors["endDown"], Colors["nightMiddle"]]}


def getDayStatus(H, M, d, m):
    times = mouthsTimes[int(m)]

    startUp, endUp, startDown, endDown = map(lambda x: x.split(":"), times.split(" "))
    totalMinits = {"sU": int(startUp[0]) * 60 + int(startUp[1]),
                   "eU": int(endUp[0]) * 60 + int(endUp[1]),
                   "dM": (int(startDown[0]) * 60 + int(startDown[1])) - (int(endUp[0]) * 60 + int(endUp[1])),
                   "sD": int(startDown[0]) * 60 + int(startDown[1]),
                   "eD": int(endDown[0]) * 60 + int(endDown[1]),
                   "nM": (int(startUp[0]) * 60 + int(startUp[1])) - (int(endDown[0]) * 60 + int(endDown[1])),
                   "now": int(H) * 60 + int(M)}
    now = totalMinits["now"]
    extraData = []
    status = 0
    if now < totalMinits["sU"]:
        status = 0
        extraData.append([0, totalMinits["sU"]])
    elif now < totalMinits["eU"]:
        status = 1
        extraData.append([totalMinits["sU"], totalMinits["eU"]])
    elif now < totalMinits["dM"]:
        status = 2
        extraData.append([totalMinits["eU"], totalMinits["dM"]])
    elif now < totalMinits["sD"]:
        status = 3
        extraData.append([totalMinits["dM"], totalMinits["sD"]])
    elif now < totalMinits["eD"]:
        status = 4
        extraData.append([totalMinits["sD"], totalMinits["eD"]])
    elif now >= totalMinits["eD"]:
        status = 5
        extraData.append([totalMinits["eD"], 24*60])
    return dayStatus[status], extraData


def colorTimeIt(timeit):
    HM, dmY = timeit.split(" ")
    H, M = HM.split(":")
    d, m, Y = dmY.split(".")
    colors, extraData = getDayStatus(H, M, d, m)
    color = "#000000"
    start, end = map(int, extraData[0])
    current = int(H) * 60 + int(M)
    sColor, eColor = colors
    colors = linear_gradient(sColor, eColor, end - start + 1)["hex"]
    color = colors[current - start]
    res = f"<font color={color}>{timeit}</font>"
    return res


# @app.route('/')
def hello_world(d, m, Y, H, M, now):
    status = ""
    Y, m, d, H, M = now.strftime("%Y:%m:%d:%H:%M").split(":")
    deltadt = now - support
    delta = int(deltadt.days) % 4 + 1
    timeit = f"{H}:{M} {d}.{m}.{Y}"
    timeit = colorTimeIt(timeit)
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
        status += timeit + "<br>status = <font color=red>Дневной</font> &#x1F506"
    elif delta == 2:
        if H < 19:
            status = "Лёха дома.<br>"
        if H >= 19:
            status = "Лёха на ночной.<br>"
        status += timeit + "<br>status = <font color=gray>Ночная</font> &#127769"
    elif delta == 3:
        if H <= 8:
            status = "Лёха на ночной.<br>"
        elif H > 8:
            status = "Лёха спит(дома).<br>"
        status += timeit + "<br>status = <font color=gray>Отсыпной</font> &#128719"
    elif delta == 4:
        status = "Лёха дома.<br>" + timeit + "<br>status = <font color=green>Выходной</font> " \
                                             "<font color=red>&#x262D</font>"
    return f"""
<html>
<head>
    <title>WhenLehaSleep</title>
</head>
<body>
<h1 align="Center">
    <font size=32>
        {status}
    </font>
</h1>
</body>
</html>"""


@app.route('/')
def hello_world_adapter():
    return hello_world2("")


@app.route('/<string:data>')
def hello_world2(data):
    status = ""
    now = datetime.datetime.now() + datetime.timedelta(hours=3)
    d, m, Y, H, M = now.strftime("%d:%m:%Y:%H:%M").split(":")
    if not data or data == "favicon.ico":
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
    elif data.count(":") == 3:
        d, m, Y, H = data.split(":")
        now = now.strptime(f"{d}:{m}:{Y}:{H}:{M}", "%d:%m:%Y:%H:%M")
        return hello_world(d, m, Y, H, M, now)
    elif data.count(":") == 4:
        d, m, Y, H, M = data.split(":")
        now = now.strptime(f"{d}:{m}:{Y}:{H}:{M}", "%d:%m:%Y:%H:%M")
        return hello_world(d, m, Y, H, M, now)
    else:
        return hello_world(d, m, Y, H, M, now)


if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except Exception as f:
        ln = len(str(f)) if chr(10) not in str(f) else max(map(len, str(f).split(chr(10))))
        print(f"ERROR:\n{'-' * ln}\n{f}\n{'-' * ln}")

