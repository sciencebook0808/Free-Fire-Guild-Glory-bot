from flask import Flask
import threading
import main

app = Flask(__name__)

@app.route("/")
def home():
    return "Free Fire Guild Glory Bot Running"

def run_bot():
    try:
        main
    except Exception as e:
        print(e)

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run()
