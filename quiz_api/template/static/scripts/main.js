const pathname = window.location.pathname;
const segments = pathname.split('/');
const game_id = segments.pop() || segments.pop();
const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username');

const ws = new WebSocket(`ws://${window.location.host}/game/${game_id}`)
ws.onopen = function(event) {
    console.log('WebSocket is open now.');
    ws.send(username)
};

function isJSON(str) {
    try {
        JSON.parse(str);
        return true;
    } catch (e) {
        return false;
    }
}


document.addEventListener('click', function(event) {
    if (event.target.classList.contains('answer')) {
        const buttons = document.querySelectorAll('.answer');
        buttons.forEach((button, index) => {
            if (button === event.target) {
                const headers = {"type": "check_answer"};
                index++;
                ws.send(JSON.stringify({headers, index}));
            }
        });
    }
});



ws.onmessage = function(event) {
    const message = event.data;
    if (!isJSON(message)) {
        if (message === `empty_${game_id}`){
            const Element = document.getElementById("messages");
            Element.innerText = 'Ожидание вопроса';
        }
    }
    else{
        const header = (JSON.parse(message))[`header`];
        if (header === "users"){
            if (!document.getElementById("players")){
                const element = document.getElementById("game");
                const el = document.createElement("h5");
                el.id = "players";
                el.textContent = "Игроки: ";
                element.appendChild(el);
            }
            const messagesDiv = document.getElementById('messages');
            const newMessage = document.createElement('li');
            newMessage.textContent = `${JSON.parse(message)['username']} : ${JSON.parse(message)['points']}`;
            messagesDiv.appendChild(newMessage);
        }else{
            document.getElementById('lobby').innerText = "";
            document.getElementById('players').innerText="";
            const data = JSON.parse(message);
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '';
            let newMessage = document.createElement('div');
            newMessage.innerHTML = `<br><br><h1> ${data['question_text']} </h1>`;
            messagesDiv.appendChild(newMessage);
            newMessage = document.createElement('div');
            newMessage.setAttribute('class', 'answers');
            newMessage.id = "ans";
            messagesDiv.appendChild(newMessage);
            const answers = data['answers_list']['list'];
            for (let i = 0; i < answers.length; i++){
                const messagesDiv = document.getElementById('ans');
                    const newMessage = document.createElement('button');
                    newMessage.setAttribute('class', 'answer');
                    newMessage.textContent =`${answers[i]['answer_text']}`;
                    messagesDiv.appendChild(newMessage);
            }
        }
    }
};

ws.onclose = function(event) {
    console.log('WebSocket is closed now.');
};

ws.onerror = function(error) {
    console.log('WebSocket error: ' + error);
};

function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value;

    // Create a custom header
    const headers = { "header": "Hello World" };

    // Send the message along with the header as a JSON string
    ws.send(JSON.stringify({ headers, message }));

    messageInput.value = '';
}
