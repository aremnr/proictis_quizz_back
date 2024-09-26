async function registerUser(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const data = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: formData.get('password'),
        referral_token: formData.get('referralToken')
    };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)

        });
        console.log(JSON.stringify(data))
        const result = await response.json();

        if (result.status === 'Registration Successful') {
            window.location.href = '/log';
        } else {
            alert('Registration failed: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}