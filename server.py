from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Rajdev's bot is running on Koyeb!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
