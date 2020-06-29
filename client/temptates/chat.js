//const socket = io()

let name
let textarea = document.querySelector('#textarea')
let messageArea = document.querySelector('.message__area')

let sendbtn=document.getElementById("send")

/*
textarea.addEventListener('keyup', (e) => {
    if(e.keyCode === 13) {
        sendMessage(e.target.value)
        console.log('work')
    }
})
*/
sendbtn.addEventListener((e)=>{
    cons
})

function sendMessage(message) {
    let msg = {
        user: name,
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



