# Import the required modules
import discord
import requests
import json 
import threading
from dotenv import load_dotenv
import os
import time
from flask import Flask, request, jsonify


async def response():
    url = "https://gb78e32e84bed74-db08fvx.adb.us-phoenix-1.oraclecloudapps.com/ords/produccion/meta/discord"
    response = requests.request('GET',url)
    data = response.json()
    text_message = data['items'][0]['text_message']
    return text_message

def sent_message(self,message):
    url = "https://gb78e32e84bed74-db08fvx.adb.us-phoenix-1.oraclecloudapps.com/ords/produccion/meta/discord"
    payload = json.dumps({
    "field": "discord",
    "value": {
        "recipient": {
        "id": str(message.author)
        },
        "channel": {
        "id": str(message.channel.id)
        },
        "timestamp": str(message.created_at),
        "message": {
        "mid": str(message.id),
        "text": str(message.content)
        }
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'IITA_BOT'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

class MyClient(discord.Client):
    async def on_ready(self):
       print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(message)
        print(f'Message from {message.author}: {message.content}')
        from discord.ext import commands
            # Verificar si el canal es una instancia de TextChannel
        if isinstance(message.channel, discord.TextChannel):
            print(f'El canal "{message.channel.name}" es del servidor.')
        else:
            print(f'El canal "{message.channel}" es privado.')

        if(message.author.id == 1254824318601400473):
            return 
        else: 
            sent_message(self,message)
            channel = message.channel
            respuesta = response()
            await channel.send(respuesta)
          
def thread_discord():
    intents = discord.Intents.default()
    intents.message_content =  True
    intents.messages = True
    intents.guilds = True

    client = MyClient(intents=intents)
    load_dotenv()
    token = os.getenv('TOKEN')
    client.run(token)




##channel=<DMChannel id=1255141323476963349 recipient=None>

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def handle_post():
    
    data = request.get_json()

    
    print(data)
    async def response_post():
        url = "https://gb78e32e84bed74-db08fvx.adb.us-phoenix-1.oraclecloudapps.com/ords/produccion/meta/discord"
        response = requests.request('GET',url)
        data = response.json()
        text_message = data['items'][0]['text_message']
        return text_message
    
    return jsonify({'message': 'Datos recibidos', 'data': data}), 200

if __name__ == '__main__':

    hilo1 = threading.Thread(target=thread_discord, args=())
    hilo1.daemon = True
    hilo1.start()
    number = 0
    app.run(host='0.0.0.0', port=5000)
    while True:
        time.sleep(3600)



