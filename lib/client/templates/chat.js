//import sjcl from 'sjcl'

const socket = io.connect('localhost:5000/test',{
    extraHeaders: {
        "Access-Control-Allow-Origin": "localhost:5000"
    }
  })

let chain = []

let textarea = document.querySelector('#textarea')
let messageArea = document.querySelector('.message__area')

 let sendbtn = document.getElementById("send")
 let textvalue = document.getElementById("textarea")
let url = document.URL
let username = document.getElementById("username").innerHTML
let cookievalue= document.cookie
let user_id = cookievalue.slice(-1)
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

function get_previoushash(){
  let block = chain[chain.length-1]
   return block['hash']
   //return 'test'
    
}




socket.on('connect', function() {
        console.log(socket.connected) 
        //make sure the connection is established
        socket.emit('user_id',{'data':user_id})
    });


socket.on('send_lastblock',() =>{
   ev= user_id+'_chain'
   socket.emit(ev,chain[chain.length-1])
})

/*
window.addEventListener('load',() =>{
    console.log("working")
   let mytime= Date.now()

    console.log(url.slice(-1))
    console.log(username)
    console.log(cookievalue.slice())
    console.log(mytime)
})
*/


sendbtn.addEventListener('click',(e)=>{
   block= {
    "data" : textvalue.value,
    "my_time" : Date.now(),
    "previous_hash" : get_previoushash(),
    "sender" : user_id,
    "reciver": url.slice(-1),
    }
    sendMessage(block)
})



function sendMessage(message) {
    let msg = {
        data: message['data']
    }
    // Append 
    appendMessage(msg, 'outgoing')
    textarea.value = ''
    scrollToBottom()

    // Send to server 
    console.log('----send :',message)
    socket.emit('private_message',message)
    return false

}

function appendMessage(msg, type) {
    let mainDiv = document.createElement('div')
    let className = type
    mainDiv.classList.add(className, 'message')

    let markup = `
        <p>${msg.data}</p>
    `
    mainDiv.innerHTML = markup
    messageArea.appendChild(mainDiv)
}

// Recieve messages 

socket.on('private_message', (msg) => {
    console.log("-----work private------",msg)
    appendMessage(msg, 'incoming')

    scrollToBottom()
    return false
})

socket.on('add_in_blockchain',(block)=>{
    chain.push(block)
    console.log("---------store ",block)

})

socket.on('store_block',(last)=>{
    chain.push(last)
    console.log("----------first store ",last)

})


function scrollToBottom() {
    messageArea.scrollTop = messageArea.scrollHeight
}



