from flask import Flask, render_template, request
import os
import platform
import subprocess
from threading import Thread
from python_files import zerokWh_charges, compareTwoFilesForIndexes, check_overlap

app = Flask(__name__)
FLASK_SHUTDOWN_ENDPOINT = "127.0.0.1:5000/shutdown"
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/compare', methods=['GET'])
def compare():
    return render_template('compare.html')


@app.route('/compare', methods=['POST'])
def comparePost():
    path1 = request.form['text1']
    path2 = request.form['text2']
    compareTwoFilesForIndexes.compareTwoFiles(path1, path2)
    path = path1[:path1.rindex("/") + 1]
    open_folder(path)

    return render_template('success.html')


@app.route('/overlap', methods=['GET'])
def overlap():
    return render_template('overlap.html')


@app.route('/overlap', methods=['POST'])
def overlapPost():
    path = request.form['text1']
    check_overlap.getOverlaps(path)
    path = path[:path.rindex("/") + 1]
    open_folder(path)
    return render_template('success.html')


@app.route('/zeroKwh', methods=['GET'])
def zeroKwh():
    return render_template('zeroKwh.html')


@app.route('/zeroKwh', methods=['POST'])
def zweroKwHPost():
    path = request.form['text1']
    zerokWh_charges.getZerokWhCharges(path)
    path = path[:path.rindex("/") + 1]
    open_folder(path)
    return render_template('success.html')


def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

class FlaskThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app.run(port=5000, host='127.0.0.1')

