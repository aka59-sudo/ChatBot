# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import json
import requests


MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)

dictKey = os.environ["DICT_KEY"]

database_uri = os.environ['DATABASE_URL']

dadJokeKey = os.environ["JOKE_KEY"]

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()


connects = 0

def botChatCommit(text):
    picLink = 'https://cdn.pixabay.com/photo/2015/06/12/18/31/cute-807306__480.png'
    db.session.add(models.newChats("Chat Bot (C.B.)", text, picLink));
    db.session.commit();

def connections(value):
    global connects
    if(value == 1):
        connects += 1
    elif(value == 0):
        connects -= 1



def bot_call(botfun, request):
    text = ''
    if(botfun == "!! funtranslate "):
        request = request.replace("!! funtranslate","")
        request = request.replace(" ","%20")

        url = "https://api.funtranslations.com/translate/southern-accent.json?text={}".format(request)
        response = requests.get(url)
        json_body = response.json()
        
        funtrans = json_body["contents"]
        
        text = "In a {} it looks something like this: {}".format(funtrans["translation"],funtrans["translated"])
        
        botChatCommit(text)
        
    elif(botfun == "unknown"):
        text = "This is not a valid command, use command '!! help' to find out about proper commands." 
        botChatCommit(text)
    
    elif(botfun == "!! slangcipher "):
        word = request.replace("!! slangcipher ","")
        
        url = "https://rapidapi.p.rapidapi.com/define"

        querystring = {"term": word}
        
        headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': dictKey
            }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        json_body = response.json()
        
        definition = json_body["list"][1]["definition"]
        
        text = "{}".format(definition)
        
        botChatCommit(text)
    
    elif(botfun == "!! joke"):
        url = "https://rapidapi.p.rapidapi.com/random/joke"

        headers = {
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
            'x-rapidapi-key': dadJokeKey
            }
        
        response = requests.request("GET", url, headers=headers)
        json_body = response.json()
        
        joke = json_body["body"][0]
        
        text =joke["setup"]
        botChatCommit(text)
        
        text = joke["punchline"]
        botChatCommit(text)
        
    elif(botfun == "!! about"):
        text = "Hello there, My name is Chat Bot. People call me C.B for short. \
            Enjoy your chat and use this resource responsibly. For more info \
            on the things that I can do enter *!! help*"
        botChatCommit(text)
        
    elif(botfun == "!! help"):
        text = "Howdy there, these are the commands at your disposal:" 
        botChatCommit(text)
        text = "<!! help> Shows the list of commands that I can handle. But you already know that :) (cont.)"
        botChatCommit(text)
        text = "<!! about> This command tells you a little bit about myself (cont.)"
        botChatCommit(text)
        text = "<!! joke> No one's talking? This command could help break the ice a little with some HILARIOUS jokes! (cont.)"
        botChatCommit(text)
        text = "<!! funtranslate> Wanna spice things up? This command whips a up a nifty translation of what you wrote. Remember to enter the text you want to translate after the command before hitting enter! (cont.)"
        botChatCommit(text)
        text = "<!! slangcipher> Did someone just use a slang that you don't know? Use this to help decipher that confusing puzzle. Remember to enter the slang or word after the command before hitting enter! (done)"
        botChatCommit(text)
    socketio.emit("bot call", {
        "action": botfun,
        "response": text
    })
    
    

def emit_all_messages(channel):
    all_userID = [ \
        db_message.userID for db_message in \
        db.session.query(models.newChats).all()
    ]
    
    all_messages = [ \
        db_message.message for db_message in \
        db.session.query(models.newChats).all()
    ]
    
    all_userPics = [ \
        db_message.profilePic for db_message in \
        db.session.query(models.newChats).all()
    ]
    
    
    socketio.emit(channel, {
        "allMessages": all_messages, 
        "allUserID": all_userID,
        "allPics": all_userPics
    })

@socketio.on('connect')
def on_connect():
    connections(1)
    print('Someone connected!')
    print(connects)
    socketio.emit('connections', {
        'num': connects
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    connections(0)
    print ('Someone disconnected!')
    print(connects)
    socketio.emit('connections', {
        'num': connects
    })

@socketio.on('new message input')
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    db.session.add(models.newChats(data["userID"],data["message"],data["userPic"]));
    db.session.commit();
    botCalls =["!! funtranslate ", "!! slangcipher "]
    regbotCall = ["!! about", "!! help", "!! joke"]
    
    if(data["message"] in regbotCall):
        bot_call(data["message"], '')
    elif((data["message"][0] == '!') and (data["message"][1] == '!')):
        tick = "out"
        for mess in botCalls:
            if(mess in data["message"]):
                tick = "in"
                bot_call(mess, data["message"])
        if(tick == "out"): 
            bot_call("unknown", '')
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
   

@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
