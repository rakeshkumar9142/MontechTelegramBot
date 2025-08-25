from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🚀 MonTech Telegram Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Incoming update:", data)
    # Process Telegram message here
    return {"ok": True}
