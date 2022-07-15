var editor = ace.edit("editor");
editor.setTheme("ace/theme/twilight");
document.getElementById('editor').style.fontSize='14px';
editor.session.setMode("ace/mode/python");
console.log(userName, 'joined the chat')

let cursorPos = null;
let lock = false

//send updates from text editor to other people connected using websocket
//this will be done as soon as a keystroke is made
editor.session.on('change', function(delta) {
    // console.log(lock)
    if(lock) return;
// delta.start, delta.end, delta.lines, delta.action
// console.log(delta)
// editor.getSession().getDocument().applyDeltas(delta)
chatSocket.send(JSON.stringify({"type": "editor", "text": delta, "cursor": editor.selection.getCursor()}))
});

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);

    if(data['type']=='editor'){
        {
        if(userName!=data.username){
            cursorPos = editor.selection.getCursor();
            lock = true;
            if(data['sync']){
                editor.setValue(data['text'])
                editor.clearSelection() 
            }
            else if(data['text']!=null){
                editor.getSession().getDocument().applyDeltas([data['text']])
    
            }
            lock = false;
            editor.moveCursorToPosition(cursorPos)
        }   
    
        }
    }

    else if(data['type']=='chat'){
        if(data.username){
            document.querySelector('#chat-text').innerHTML += ('<span class="text-danger">' + data.username + '</span>'+ ': ' + data.message + '<br/>')
        }
        else{
            document.querySelector('#chat-text').innerHTML += ('<span class="font-weight-bold">' + data.message + '</span>' + '<br/>') 
        }
        var xH = chatWindow.scrollHeight
        chatWindow.scrollTo(0, xH)}
    
    else if(data['type']=='output'){
        console.log("HERE")
        showOutput(data['data'])
        console.log(data)
    }
   
}


function changeFontSize(e) {
    let val = e.value
    let ele = document.getElementById('editor')
    ele.style.fontSize=`${val}px`
}


function runCode(e){
    let code = editor.getValue()
    let ele = document.getElementById('code-output');
    
    let input = document.getElementById('code-input');
    let language = document.getElementById('language').value;
    console.log("input : ",language)
    console.log("Clicked");
    console.log(code);
    ele.classList = ['text-white']
    axios.post(`/api/v1/run/${language}/`, {
        'code': code,
        'input':input.value
    },{
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(res => {
        console.log(res.data)
        JSON.stringify({
            type: "output",
            data: res,
        });
        showOutput(res)
    }).catch(err=>{
        ele.classList.add('text-danger')
        ele.innerHTML = 'Unexpected error occured'
    })
}

function showOutput(res) {
    let data = res.data
    let ele = document.getElementById('code-output')
    ele.classList = ['text-white']
    let text
    if(data.code == '0'){
        text = data.results
    }
    else if(data.code == '1'){
        ele.classList.add('text-danger')
        text = data.results
    }
    else if(data.code == '2'){
        ele.classList.add('text-danger')
        text = 'Compilation/Syntax errors!'
    }
    ele.innerHTML = text 
}

function saveCode(e) {
    console.log("pressed")
    let code = editor.getValue()
    //synchronizes the code for all clients with the code which is present with the user that presses the button
    chatSocket.send(JSON.stringify({
        type: "editor",
        text: code,
        sync: true,
    }))
}

let chatWindow = document.getElementById('chat-text');

document.querySelector('#submit').onclick = function (e) {
    console.log('sending data')
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'type': 'chat',
        'message': message,
    }));
    messageInputDom.value = '';
};



const chatSocket = new WebSocket(
    'wss://' +
    // 'ws://' +
    window.location.host +
    '/ws/code/' +
    roomName +
    '/'
);

//stop reloading page when pressed enter in chatbox, but instead click the submit button
$("#input").on('keypress', (e) => {
    if(e.key == 'Enter'){
        $("#submit").click()
    }
})

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if(data.username){
        document.querySelector('#chat-text').innerHTML += ('<span class="text-danger">' + data.username + '</span>'+ ': ' + data.message + '<br/>')
    }
    else{
        document.querySelector('#chat-text').innerHTML += ('<span class="font-weight-bold">' + data.message + '</span>' + '<br/>') 
    }
    var xH = chatWindow.scrollHeight; 
    chatWindow.scrollTo(0, xH);

}

chatSocket.onclose = (e) => {
    setTimeout(function(){
        alert("Lost connection to the server. Disconnected.")
    }, 200)
}



$(document).ready(() => {
    $("#exit").click(() => {
        chatSocket.close()
        document.querySelector('#chat-text').innerHTML += ('<span class="font-weight-bold">' + 'Connection closed.' + '</span>' + '<br/>') 
        $("#exit").hide()
        $("#submit").hide()
        $("#reload").show()
    })
    $("#reload").click(() => {
        location.reload()
    })
})