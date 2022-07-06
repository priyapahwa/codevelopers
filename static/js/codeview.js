var editor = ace.edit("editor");
editor.setTheme("ace/theme/twilight");
document.getElementById('editor').style.fontSize='14px';
editor.session.setMode("ace/mode/python");

let cursorPos = null;
let lock = false



onmessage = function (e) {
    let data = JSON.parse(e.data);

    if(data['type']=='editor'){
        {
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
    console.log("Clicked");
    console.log(code);
    ele.classList = ['text-white']
    let url = '/code/run/'
    axios.post(url, {
        'code': code,
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