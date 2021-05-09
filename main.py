from flask import Flask, jsonify
import json
from pc_generator.spiders import microcenter_spider


app = Flask(__name__)


@app.route('/')
def index():
    with open("parts.json", "r") as open_file:
        file = json.load(open_file)
        open_file.close()

    return jsonify(file)


if __name__ == '__main__':
    app.run()
