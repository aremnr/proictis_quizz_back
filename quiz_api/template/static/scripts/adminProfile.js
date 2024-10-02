quiz_div = document.getElementById("quizzes")
quizzes = JSON.parse(localStorage.getItem('quizzes'))
for (let i = 0; i < quizzes.length; i++) {
    quiz_id_button = document.createElement("button")
    quiz_id_button.setAttribute('class', 'hidden-button')
    quiz_id_button.setAttribute('onclick', 'copyText(this)')
    quiz_id_button.id = `${quizzes[i].id}`
    quiz_id_button.textContent = `${quizzes[i].name}`
    quiz_div.appendChild(quiz_id_button)
}
function copyText(button) {
    const tempInput = document.createElement("input");
    tempInput.value = button.id;
    button_text = button.innerText
    document.body.appendChild(tempInput);

    tempInput.select();
    document.execCommand("copy");

    document.body.removeChild(tempInput);

    button.innerText = "Скопировано!";

    setTimeout(() => {
        button.innerText = button_text;
    }, 2000);
}

document.getElementById('GoTOCreate').addEventListener('click', function () {
    window.location.href = "/create_quiz";
})


document.getElementById('create-referral-btn').addEventListener('click', function() {
    const token = localStorage.getItem('authToken');
    fetch('/create_referral', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
            if (response.status === 401){
                alert("Истек срок действия токена. Перезайдите в систему, пожалуйста.")
                window.location.href= "/log"
            }
            if (response.ok){
                return response.json()
            }
        }
    )
    .then(data => {
        const referralResult = document.getElementById('referral-result');
        referralResult.textContent = `Referral: ${data.referral}`;
        referralResult.classList.remove('hidden');
    })
    .catch(error => console.error('Error:', error.message));
});

document.getElementById('create-game-btn').addEventListener('click', function() {
    const gameForm = document.getElementById('game-form');
    gameForm.classList.remove('hidden');
});

document.getElementById('submit-game-btn').addEventListener('click', function() {
    const quizId = document.getElementById('quiz-id-input').value;
    const token = localStorage.getItem('authToken');
    fetch(`/create_game?quiz_id=${quizId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 401){
            alert("Истек срок действия токена. Перезайдите в систему, пожалуйста.")
            window.location.href="/log"
        }
        if (response.ok){
            return response.json()
        }
    })
    .then(data => {
        const gameResult = document.getElementById('game-result');
        const gameButton = document.getElementById("go-to-admin-page-btn");
        const qrcode = document.getElementById("qrcode");
        gameButton.classList.remove('hidden')
        gameResult.classList.remove('hidden')
        qrcode.classList.remove('hidden')
        qrcode.append(QRCreator(`http://${window.location.host}/user_add/${data.game_id}`).result);
        localStorage.setItem('gameId', `${data.game_id}`)
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('go-to-admin-page-btn').addEventListener('click', function () {
    game_id = localStorage.getItem('gameId')

    token = localStorage.getItem('authToken')
    fetch(`/admin_game/${game_id}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (response.status === 401){
                    alert("Истек срок действия токена. Перезайдите в систему, пожалуйста.")
                    window.location.href="/log"
                }
                if (response.ok) {
                    return response.text();
                }
                throw new Error('Network response was not ok.');
            })
            .then(html => {
                document.open();
                document.write(html);
                document.close();
            })
            .catch(error => {
                console.error('Fetch operation failed: ', error);
            });

})