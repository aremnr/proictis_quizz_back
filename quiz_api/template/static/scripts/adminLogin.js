async function loginUser(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const data = new URLSearchParams();
    data.append('grant_type', '');
    data.append('username', formData.get('username'));
    data.append('password', formData.get('password'));
    data.append('scope', '');
    data.append('client_id', '');
    data.append('client_secret', '');

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        const result = await response.json();

        if (response.ok) {
            const accessToken = result.access_token;
            const token = `${accessToken}`;

            localStorage.setItem('authToken', token);

            fetch('/profile', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (response.ok) {
                    fetch('/temp', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    }).then(response => response.json())
                        .then(response => {
                            localStorage.setItem('quizzes', JSON.stringify(response.quizzes));
                            }
                        );
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

        } else {
            alert('Login failed: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}