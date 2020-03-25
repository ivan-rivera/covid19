from decouple import config
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World 3!"


if __name__ == '__main__':
    PORT = config(
        "PORT", default=8000, cast=int)
    app.run(host="0.0.0.0", port=PORT)
