
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>calculator Application Running Successfully</h1>"

if __name__ == "__main__":
    app.run(port=5001)
