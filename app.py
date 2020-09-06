# coding: utf-8
from flask import Flask
from flask import request
import coolpoko as poko

app = Flask(__name__)

@app.route('/')
def main():
    s = poko.create_sentence()
    return s[0] + '\n' + s[1]

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8000")