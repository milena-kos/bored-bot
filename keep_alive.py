from flask import Flask, current_app
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return current_app.send_static_file('main.html')

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()