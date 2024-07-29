import os 
import requests
import telebot
import json

BOT_TOKEN = os.environ.get('BOT_TOKEN')
PASSWORD = os.environ.get('PASSWORD')

bot = telebot.TeleBot(BOT_TOKEN)

users_set = []

response = requests.get('http://ipinfo.io/ip')
stats_response = requests.get('http://localhost:5000/metrix')
stats_json = stats_response.json()
stats = ''
for key, value in stats_json.items():
    stats += f' | {key}: {value}\n'

with open('users.txt', 'r') as file:
    for line in file:
        users_set.append(line)

for user in users_set:
    try:
        bot.send_message(user, f'Current ip: {response.text.strip()}\nJenkins: http://{response.text.strip()}:20808\nStats:\n{stats}')
    except:
        continue



@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in users_set:
        with open('users.txt','w') as file:
            file.write(f"{chat_id}\n")
    bot.reply_to(message, "Льоня на связі")
@bot.message_handler(commands=['get_info'])
def get_info(message):
    response = requests.get('http://ipinfo.io/ip')
    stats_response = requests.get('http://localhost:5000/metrix')
    stats_json = stats_response.json()
    stats = ''
    for key, value in stats_json.items():
        stats += f' | {key}: {value}\n'
    bot.reply_to(message, f'Current ip: {response.text.strip()}\nJenkins: http://{response.text.strip()}:20808\nStats:\n{stats}' )

bot.infinity_polling()