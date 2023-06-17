from flask import Flask
from flask import render_template
import subprocess
import datetime
import re
import json 
app = Flask(__name__)

@app.route("/")
def index():
    timings = json.loads(data())
    return render_template("index.html", **timings)

@app.route("/data")
def data():
    line = subprocess.run(
        "ps -p $(pgrep -f ^/usr/bin/python3.*Sardana.*scattering) -o etimes",
        shell=True,
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8")
    search = re.search(r"ELAPSED\n +(\d+)", line)
    seconds = 0
    timings = {"D" : "?", "H": "?", "M":"?"}
    if search is not None:
        seconds = search.group(1)
        td = datetime.timedelta(seconds=int(seconds))
        timings["D"] = td.days
        timings["H"] =  td.seconds // 3600
        timings["M"] = (td.seconds // 60) % 60
    return json.dumps(timings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)