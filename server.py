from threading import Thread
from flask import Flask
app = Flask('')


@app.route('/')
def home():
    return "Hello"


def run():
    app.run(host='0.0.0.0', port=8888)


def Server():
    n = Thread(target=run)
    n.start()
