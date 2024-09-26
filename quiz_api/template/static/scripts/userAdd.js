const username = document.getElementById('username').value;
const pathname = window.location.pathname;
const segments = pathname.split('/');
const game_id = segments.pop() || segments.pop();

function redirect(url) {
    window.location.href = url;
}

document.addEventListener('click', function(event) {
    if (event.target.tagName === 'BUTTON') {
        const username = document.getElementById('username').value;
        const url = `http://${window.location.host}/game/${game_id}?username=${username}`;
        redirect(url);
    }
});
