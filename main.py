# Import the required modules
import discord
from discord.ext import commands
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
    if isinstance(message.channel, discord.TextChannel):
           payload = json.dumps({
                                "field": "discord",
                                "value": {
                                        "sender":"TextChannel",
                                        "author": {
                                                    "id": str(message.author.id),
                                                    "name": str(message.author.name),
                                                    "global_name":str(message.author.global_name)
                                        },
                                        "channel": {
                                                    "id": str(message.channel.id),
                                                    "name":str(message.channel.name),
                                                    "position":str(message.channel.position),
                                                    "nsfw":str(message.channel.nsfw),
                                                    "category_id":str(message.channel.category_id)
                                        },
                                        "message": {
                                            "mid": str(message.id),
                                            "text": str(message.content),
                                            "timestamp": str(message.created_at)
                                        }
                                    }
                                })
    else:
        payload = json.dumps({
                                "field": "discord",
                                "value": {
                                        "sender":"DMChannel",
                                        "author": {
                                                    "id": str(message.author.id),
                                                    "name": str(message.author.name),
                                                    "global_name":str(message.author.global_name)
                                        },
                                        "channel": {
                                                    "id": str(message.channel.id),
                                                    "recipient":str(message.channel.recipient)
                                        },
                                        "message": {
                                            "mid": str(message.id),
                                            "text": str(message.content),
                                            "timestamp": str(message.created_at)
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
        print(f'Message from {message.author}: {message.content}')
        print(message)
        if(message.author.id == 1254824318601400473):
            return 
        else: 
            sent_message(self,message)
            channel = message.channel
            respuesta = await response()
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

def thread_send_message():
    intents = discord.Intents.default()
    TOKEN = os.getenv('TOKEN')
    ##intents.message_content =  True
    ##intents.messages = True
    intents.members = True
    ##intents.guilds = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'Conectado como {client.user}')
        ##channel_id = 1255141323476963349
        ##channel = client.get_channel(channel_id)
        ##WITH REFERRAL
        ##message_id = 1  
        ##message_reference = discord.MessageReference(message_id=message_id, channel_id=channel_id, fail_if_not_exists=False)
        ##await channel.send('Respuesta al mensaje anterior', reference=message_reference)
        ##await channel.send('MENSAJE DESDE EL POST')
        ##user_id = 123456789012345678  # Reemplaza con el ID del usuario

    # Obtener al usuario por su ID
        user = await client.fetch_user(749001989232394341)

        if user:
            try:
                # Enviar el mensaje privado
                message = await user.send('¡Hola! Este es un mensaje privado.')
                print(f'Mensaje enviado a {user.name}')
                print("-----------------------------------------------------------")
                print("Mensaje enviado: ",message)
                print("-----------------------------------------------------------")
            except discord.Forbidden:
                print('No tengo permisos para enviar un mensaje privado a este usuario.')
                return 
            except discord.HTTPException as e:
                print(f'Error al enviar el mensaje: {e}')
        else:
            print('Usuario no encontrado.')
        # Cerrar la sesión del bot después de enviar el mensaje
    
        await client.close()

    # Iniciar el bot
    client.run(TOKEN)

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def handle_post():
    
    data = request.get_json()
    print(data)
    
    response = thread_send_message()
    
    return jsonify({'message': 'Datos recibidos', 'data': data}), 200

if __name__ == '__main__':

    hilo1 = threading.Thread(target=thread_discord, args=())
    hilo1.daemon = True
    hilo1.start()
    app.run(host='0.0.0.0',port=5000)
    
    while True:
        time.sleep(3600)



"""
payload = json.dumps({
                                "field": "discord",
                                "value": {
                                        "sender":"TextChannel||DMChannel",
                                        },
                                        "message": {
                                            "type" : text,
                                            "mid": mid,
                                            "text": text,
                                            "channel_id" : id || "author_id" : id       
                                        }
                                    }
                                })
"""