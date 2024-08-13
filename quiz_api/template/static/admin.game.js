const game_id = localStorage.getItem("gameId")
const ws = new WebSocket(`ws://localhost:9090/game/${game_id}`)
ws.onopen = function(event) {
    console.log('WebSocket is open now.');
    ws.send(`${localStorage.getItem('authToken')}`)
};

function isJSON(str) {
    try {
        JSON.parse(str);
        return true;
    } catch (e) {
        return false;
    }
}

ws.onmessage = function(event) {
    const message = event.data;
    if (isJSON(message)) {
        const header = (JSON.parse(message))[`header`];
        if (header === "Answer_check"){
            const answer = JSON.parse(message)[`Answer`];
            const messagesDiv = document.getElementById("main");
            const newMessage = document.createElement('h1');
            newMessage.textContent = answer;
            newMessage.id = "answer_line";
            newMessage.setAttribute("style", "top: 150px; text-align: center");
            messagesDiv.appendChild(newMessage);
        }
        else if (header === "delete") {
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = ' ';
            const button = document.getElementById('button');
            button.remove();
            const el = document.getElementById('answer_line');
            el.remove()
        } else if (header === "users"){
            const messagesDiv = document.getElementById('messages');
            const newMessage = document.createElement('li');
            newMessage.id = JSON.parse(message)['username'];
            newMessage.textContent = `${JSON.parse(message)['username']} : ${JSON.parse(message)['points']}`;
            messagesDiv.appendChild(newMessage);
        } else if (header === "user_update") {
            const newMessage = document.getElementById(`${JSON.parse(message)['username']}`);
            newMessage.textContent = `${JSON.parse(message)['username']} : ${JSON.parse(message)['points']}`;
        } else if (header === "end_game") {
            const button = document.getElementById('button');
            button.textContent = "END GAME";
        }
    }
};

document.addEventListener('click', function(event) {
    if (event.target.tagName === 'BUTTON') {
        const message = event.target.textContent;
        if (message === "Start" || message === "Next") {
            if (document.getElementById('answer_line')){
                const el = document.getElementById('answer_line');
                el.remove()
            }
            const headers = {"type": "game"};
            ws.send(JSON.stringify({headers}));
            const button = document.getElementById('button');
            button.setAttribute("class", "answer");
            button.setAttribute("style", "width: 400px; margin-left: 10px");
            button.textContent = 'Show Right Answer';
        } else if (message === "Show Right Answer"){
            const headers = {"type": "get_answer"};
            const button = document.getElementById('button');
            button.textContent = 'Next';
            ws.send(JSON.stringify({headers}));
        } else if (message === "END GAME"){
            const headers = {"type": "end_game"};
            ws.send(JSON.stringify({headers}));
        }

    }

});
