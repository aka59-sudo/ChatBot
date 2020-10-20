    
import * as React from 'react';

import { Button } from './Button';
import { Socket } from './GoogleButton';
import { isBot } from './Bot';
import { profilePic } from './GoogleButton';

export function Content() {
    const [botMess, setBotMess] = React.useState('')
    const [connections, setConnections] = React.useState(0);
    const [messages, setMessages] = React.useState([]);
    const [userID, setUserID] = React.useState([]);
    const [userPic, setUserPic] = React.useState([]);
    
    
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
        setUserPic(data['allPics'])
    }
    
    
    function checkPIC(url) {
        return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
    }
    
    function validURL(str) {
      var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
        '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
      return !!pattern.test(str);
    }
    
    function giveHTML(message, index) {
        if(checkPIC(message)){
            return( <li id={ userID[index] } key={ index }><img src={ userPic[index] } id="profPic"/>{userID[index]}: <b><img src={ message }/></b></li>)
        }else if(validURL(message)){
            if(message.startsWith("http")){
                 return( <li id={ userID[index] } key={ index }><img src={ userPic[index] } id="profPic"/>{userID[index]}: <b><a href={ message }>{ message }</a></b></li>)
            }
            else{
                return( <li id={ userID[index] } key={ index }><img src={ userPic[index] } id="profPic"/>{userID[index]}: <b><a href={'https://' + message }>{ message }</a></b></li>)
            }
        }else{
            return( <li id={ userID[index] } key={ index }><img src={ userPic[index] } id="profPic"/>{userID[index]}: <b>{ message }</b></li>)
        }
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
                        messages.map((message, index) => giveHTML(message, index))
                        
                    }
                </ol>
            <Button />
        </div>
    );
}
