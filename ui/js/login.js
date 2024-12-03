document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    const loginContainer = document.getElementById('loginContainer');
    const registerContainer = document.getElementById('registerContainer');

    showRegisterLink.addEventListener('click', function(e) {
        e.preventDefault();
        loginContainer.style.display = 'none';
        registerContainer.style.display = 'block';
    });

    showLoginLink.addEventListener('click', function(e) {
        e.preventDefault();
        loginContainer.style.display = 'block';
        registerContainer.style.display = 'none';
    });

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            if (response.ok) {
                window.location.href = 'index.html';
            } else {
                alert(data.message || 'Login failed');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during login');
        }
    });

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = {
            name: document.getElementById('regName').value,
            email: document.getElementById('regEmail').value,
            password: document.getElementById('regPassword').value
        };

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            if (response.ok) {
                alert('Registration successful! Please login.');
                loginContainer.style.display = 'block';
                registerContainer.style.display = 'none';
            } else {
                alert(data.message || 'Registration failed');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during registration');
        }
    });
});
