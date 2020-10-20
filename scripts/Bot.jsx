import * as React from 'react';
import { Socket } from './GoogleButton';



export function isBot(data){
    var message = data["action"]
    var about = "!! about"
    var help = "!! help"
    var translate = "!! funtranslate "
    var dadjoke = "!! joke"
    var slangcipher = "!! slangcipher "
    var unknown = "unknown"
    
    if(message == about){
        console.log("Bot About")
        botAbout()
    }
    if(message == help){
        console.log("Bot Help")
        botHelp()
    }
    if(message == translate){
        console.log("Bot Translate")
        console.log('Sent the bot translate message to server!');
    }    
    if(message == dadjoke){
        console.log("dadjoke")
        console.log('Sent the bot joke message to server!');
    }  
    if(message == slangcipher){
        console.log("slang")
        console.log('Sent the bot slang message to server!');
    }
    if(message == unknown){
        console.log("Bot Unknown")
        console.log('Sent the bot unknown message to server!');
    }
}



function botAbout() {
    
    var text = "Hello there, My name is Chat Bot. People call me C.B for short. \
            Enjoy your chat and use this resource responsibly. For more info \
            on the things that I can do enter *!! help*"
            
    
    console.log('Sent the bot about message to server!');
}

function botHelp() {
    console.log('Sent the bot help message to server!');
}


