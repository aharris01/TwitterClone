document.getElementById('loginForm').addEventListener('submit', function (event) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        event.preventDefault();
        alert('Username and password are required');
        return false;
    }

    const re = new RegExp("^[A-Za-z0-9_-]{1,32}$");
    if (!re.test(username)) {
        event.preventDefault();
        alert('Username contains invalid characters');
        return false
    }
    return true;
});