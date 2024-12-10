# import speech_recognition as sr
# import websocket
# import requests

# r = sr.Recognizer()

# def send_command_to_esp32(command):
#     websocket_url = "ws://192.168.12.113:81"  # Replace with your ESP32 WebSocket server URL
#     ws = websocket.create_connection(websocket_url)
#     ws.send(command)
#     ws.close()

# def convert_text_to_command(text):
#     # Replace this URL with your API endpoint
#     api_url = "http://dgx.kmitonline.in:4000/"
    
#     # Assuming the API expects a JSON payload with the text
#     payload = {"input": text}
    
#     try:
#         response = requests.post(api_url, json=payload)
#         if response.status_code == 200:
#             output = response.json()["output"]
#             return output.strip()  # Remove any leading/trailing whitespace
#         else:
#             print("Failed to get a valid response from the API.")
#             return None
#     except Exception as e:
#         print("Error occurred during API call:", e)
#         return None

# def recognize_speech():
#     with sr.Microphone() as source:
#         print("Say something!")
#         audio = r.listen(source)

#     try:
#         text = r.recognize_google(audio)
#         print("You said: " + text)
        
#         # Convert recognized text to command using the API
#         command = convert_text_to_command(text)
#         if command is not None:
#             if command == "1":
#                 send_command_to_esp32("on")
#                 print("Sent 'on' command to ESP32")
#             else:
#                 send_command_to_esp32("off")
#                 print("Sent 'off' command to ESP32")

#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))

# # Continuously listen for speech
# send_command_to_esp32("off")
# while True:
#     recognize_speech()



import speech_recognition as sr
import serial
import websocket
import time
import os
import requests
import json
r = sr.Recognizer()

# Your OpenAI API key
api_key = 'API KEY'
url = 'https://api.openai.com/v1/chat/completions'
def classify(str):
    prompt = str+" --   suggest me whether to on or off the bulb based on the statement , just tell me in one word [off, on]"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }


    data = {
    'model': 'gpt-3.5-turbo',  # Replace with the current model name
    'messages': [
        {'role': 'user', 'content': prompt},
    ]
}


    json_data = json.dumps(data)
    response = requests.post(url, headers=headers, data=json_data)

    if response.status_code == 200:
        model_output = response.json()['choices'][0]['message']['content']
        return model_output
    else:
        print(f"Error: {response.status_code}\n{response.text}")


def send_command_to_esp32(command):
    websocket_url = "ws://192.168.87.1:XX"  # Replace with your ESP32 WebSocket server URL
    ws = websocket.create_connection(websocket_url)
    ws.send(command)
    ws.close()

def recognize_speech():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        # text = r.recognize_sphinx(audio)
        text=classify(text)
        print("You said: " + text)
        if "on" in text:
            # ser.write(b'1')  # Sending '1' to turn on the LED
            send_command_to_esp32("on")
            print('Sent 1')
        elif "off" in text:
            # ser.write(b'0')  # Sending '0' to turn off the LED
            send_command_to_esp32("off")
            print('Sent 0')


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Continuously listen for speech
send_command_to_esp32("off")
while True:
    recognize_speech()