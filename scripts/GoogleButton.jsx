import * as React from 'react';
import ReactDOM from 'react-dom';
import { Content } from './Content';
import GoogleLogin from 'react-google-login';
import * as SocketIO from 'socket.io-client';

export var Socket
export var googName
export var profilePic

const responseGoogle = (response) => {
  console.log(response.profileObj);
}
 
function handleSubmit(response) {
    console.log(response.profileObj.name + 'handlerrrr');
    googName = response.profileObj.name
    profilePic = response.profileObj.imageUrl
    // TODO replace with name from oauth
    Socket = SocketIO.connect();
    ReactDOM.render(<Content />, document.getElementById('content'));
}

export function GoogleButton() {
    return  <GoogleLogin
            clientId="316604030096-a66nlesv0inobncfd9rcbuqjg9ahpd56.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={handleSubmit}
            onFailure={responseGoogle}
            cookiePolicy={'single_host_origin'}
            />
}
