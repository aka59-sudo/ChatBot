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

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()


connects = 0
def connections(value):
    global connects
    if(value == 1):
        connects += 1
    elif(value == 0):
        connects -= 1



def bot_call(botfun, request):
    text = ''
    if(botfun == "!! funtranslate "):
        request = request.lstrip("!! funtranslate")
        request = request.replace(" ","%20")

        url = "https://api.funtranslations.com/translate/southern-accent.json?text={}".format(request)
        response = requests.get(url)
        json_body = response.json()
        
        funtrans = json_body["contents"]
        
        text = "In a {} it looks something like this: {}".format(funtrans["translation"],funtrans["translated"])
    
    
    elif(botfun == "!! slangcipher "):
        print("in DICT")
        word = request.lstrip("!! slangcipher ")
        print("Word " + word)
        
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
        
        
       
    socketio.emit("bot call", {
        "action": botfun,
        "response": text
    })
    
    

def emit_all_messages(channel):
    all_userID = [ \
        db_message.userID for db_message in \
        db.session.query(models.Chats).all()
    ]
    
    all_messages = [ \
        db_message.message for db_message in \
        db.session.query(models.Chats).all()
    ]
    
    socketio.emit(channel, {
        "allMessages": all_messages, 
        "allUserID": all_userID
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
    db.session.add(models.Chats(data["userID"],data["message"]));
    db.session.commit();
    botCalls =["!! funtranslate ", "!! slangcipher "]
    regbotCall = ["!! about", "!! help", "!! dadjoke"]
    
    if(data["message"] in regbotCall):
        bot_call(data["message"], '')
    elif((data["message"][0] == '!') and (data["message"][1] == '!')):
        print("IN CHECKER")
        tick = "out"
        for mess in botCalls:
            if(mess in data["message"]):
                tick = "in"
                print("Active")
                bot_call(mess, data["message"])
        if(tick == "out"): 
            print("IN  UNKNOWN")
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
