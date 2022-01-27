let socket = io.connect("http://127.0.0.1:5000")
// const logout = document.querySelector("[data-logout]")

let msgInput = document.getElementById("msg")
let sendBtn = document.getElementById("send-btn")
let msgsContainer = document.getElementById("msgs-container")

socket.on("connect",()=>{
    socket.emit("conn",id)
})

// logout.addEventListener("click",()=>{
//     socket.emit("disconn",id)
// })


sendBtn.addEventListener("click",()=>{
    
    const data = {
        sender : id,
        reciever : reciever,
        msgBody : msgInput.value
    }
    const mineMsgDiv = document.createElement("div")
    mineMsgDiv.classList.add("mine-msg")
    const msgContentDiv = document.createElement("div")
    msgContentDiv.classList.add("msg-content")
    const h2 = document.createElement("h2")
    h2.innerText = username
    const h3 = document.createElement("h3")
    h3.innerText = msgInput.value
    msgContentDiv.append(h2)
    msgContentDiv.append(h3)
    mineMsgDiv.append(msgContentDiv)
    msgsContainer.insertBefore(mineMsgDiv,msgsContainer.firstChild)
    // var container = document.getElementById('pcontainer');
    // container.insertBefore(document.createElement("p"), container.firstChild);
    msgInput.value = ""
    socket.emit("msg",data)
})

socket.on("msg",(data)=>{

    const otherMsgDiv = document.createElement("div")
    otherMsgDiv.classList.add("other-msg")
    const msgContentDiv = document.createElement("div")
    msgContentDiv.classList.add("msg-content")
    const h2 = document.createElement("h2")
    h2.innerText = data.username
    const h3 = document.createElement("h3")
    h3.innerText = data.msgBody
    msgContentDiv.append(h2)
    msgContentDiv.append(h3)
    otherMsgDiv.append(msgContentDiv)
    msgsContainer.insertBefore(otherMsgDiv,msgsContainer.firstChild)
})

