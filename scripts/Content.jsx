    
import * as React from 'react';

import { Button } from './Button';
import { Socket } from './Socket';
import { isBot } from './Bot';

export function Content() {
    const [botMess, setBotMess] = React.useState('')
    const [connections, setConnections] = React.useState(0);
    const [messages, setMessages] = React.useState([]);
    const [userID, setUserID] = React.useState([]);
    
    
    function Bot() {
        React.useEffect(() => {
            Socket.on('bot call', isBot);
            return () => {
                Socket.off('bot call', isBot);
            }
        });
    }
    
    
    
    function numConnections() {
        React.useEffect(() => {
            Socket.on('connections', connectCount);
            return () => {
                Socket.off('connections', connectCount);
            }
        });
    }
    
    function connectCount(data){
        var connects = data["num"]
        console.log("This is the number" + data["num"])
        if(connections != connects){
            setConnections(connects)
        }
    }
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('messages received', updateMessages);
            return () => {
                Socket.off('messages received', updateMessages);
            }
        });
    }
    
    function updateMessages(data) {
        console.log(Socket.io.engine.id)
        console.log("Received messages from server: " + data['allMessages']);
        setMessages(data['allMessages']);
        setUserID(data['allUserID'])
    }
    
    Bot();
    getNewMessages();
    numConnections();
    

    return (
        <div>
            <h1>Chat Room!</h1>
            <h3>Connected Users: {connections}</h3>
                <ol id="myList">
                    {   
                        messages.map(
                        (message, index) => <li id={ userID[index] } key={ index }>{userID[index]}: <b>{ message }</b></li>)
                    }
                </ol>
            <Button />
        </div>
    );
}
