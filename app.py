# coding: utf-8
from flask import Flask
import coolpoko_markov as poko

app = Flask(__name__)

@app.route('/')
def main():
    return "Hello world!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8000")