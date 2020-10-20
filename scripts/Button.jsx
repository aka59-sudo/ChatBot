import * as React from 'react';
import { Socket } from './GoogleButton';
import { googName } from './GoogleButton'
import { profilePic } from './GoogleButton';


function handleSubmit(event) {
    let newMessage = document.getElementById("message_input");
    // TODO send the address on socket to server
    Socket.emit('new message input', {
        "message": newMessage.value,
        "userID": googName,
        "userPic": profilePic
    });
    console.log('Sent the message ' + newMessage.value + ' to server!');
    newMessage.value = ''
    
    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="message_input" placeholder="Enter a Message"></input>
            <button>Add Message!</button>
        </form>
    );
}
