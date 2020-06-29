const socket = io.connect('localhost:5000/test',{
    extraHeaders: {
        "Access-Control-Allow-Origin": "localhost:5000"
    }
  })


let textarea = document.querySelector('#textarea')
let messageArea = document.querySelector('.message__area')

 let sendbtn = document.getElementById("send")
 let textvalue = document.getElementById("textarea")
let url = document.URL
let username = document.getElementById("username").innerHTML
let cookievalue= document.cookie
/*
textarea.addEventListener('keyup', (e) => {
    if(e.keyCode === 13) {
        sendMessage(e.target.value)
        console.log('work')
    }
})
 socket.on('connect', function() {
        console.log(socket.connected) //make sure the connection is established
    });
*/
socket.on('connect', function() {
        console.log(socket.connected) //make sure the connection is established
    });
window.addEventListener('load',() =>{
    console.log("working")

    console.log(url.slice(-1))
    console.log(username)
    console.log(cookievalue.slice(-1))
})
sendbtn.addEventListener('click',(e)=>{
    msg = textvalue.value;
    sendMessage(msg)
})

function sendMessage(message) {
    let msg = {
        message: message.trim()
    }
    // Append 
    appendMessage(msg, 'outgoing')
    textarea.value = ''
    scrollToBottom()

    // Send to server 
   // socket.emit('message', msg)

}

function appendMessage(msg, type) {
    let mainDiv = document.createElement('div')
    let className = type
    mainDiv.classList.add(className, 'message')

    let markup = `
        <h4>${msg.user}</h4>
        <p>${msg.message}</p>
    `
    mainDiv.innerHTML = markup
    messageArea.appendChild(mainDiv)
}

// Recieve messages 
/*
socket.on('message', (msg) => {
    appendMessage(msg, 'incoming')
    scrollToBottom()
})
*/

function scrollToBottom() {
    messageArea.scrollTop = messageArea.scrollHeight
}



