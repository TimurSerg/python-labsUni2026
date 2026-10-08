from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/currency")
def currency():
    key = request.args.get("key")
    today = "today" in request.args
    print(f"today={today}, key={key}, all par={dict(request.args)}")
    return "USD - 45"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)