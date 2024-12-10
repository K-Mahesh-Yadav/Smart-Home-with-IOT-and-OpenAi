import asyncio
import websockets
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

async def send_receive_message(message):
    uri = "ws://192.168.1XX.XX:XX"  # Replace with your server IP address

    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response

@app.route("/control", methods=["POST"])
def control():
    action = request.form["action"]
    
    if action == "on" or action == "off":
        response = asyncio.get_event_loop().run_until_complete(send_receive_message(action))
        return response
    else:
        return "Invalid action"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
