from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory("html", "index.html")

if __name__ == '__main__':
    app.run(debug=True, host="192.168.0.123", port=80)