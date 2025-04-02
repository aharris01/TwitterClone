document.getElementById('new_password').addEventListener('input', function () {
    const password = this.value;
    const strengthBar = document.getElementById('passwordStrengthBar');
    const feedback = document.getElementById('passwordFeedback');

    // Check password strength
    const hasLowercase = /[a-z]/.test(password);
    const hasUppercase = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    const isLongEnough = password.length >= 8;

    const strength = [hasLowercase, hasUppercase, hasNumber, hasSpecial, isLongEnough].filter(Boolean).length;

    // Update strength bar
    strengthBar.className = 'password-strength-bar';
    if (strength <= 2) {
        strengthBar.classList.add('weak');
        strengthBar.style.width = '33%';
        feedback.textContent = 'Weak password';
        feedback.style.color = '#ff4d4d';
    } else if (strength <= 4) {
        strengthBar.classList.add('medium');
        strengthBar.style.width = '66%';
        feedback.textContent = 'Medium strength password';
        feedback.style.color = '#ffb84d';
    } else {
        strengthBar.classList.add('strong');
        strengthBar.style.width = '100%';
        feedback.textContent = 'Strong password';
        feedback.style.color = '#4CAF50';
    }
});

document.getElementById('confirm_password').addEventListener('input', function () {
    const newPassword = document.getElementById('new_password').value;
    const confirmPassword = this.value;
    const feedback = document.getElementById('confirmPasswordFeedback');

    if (newPassword === confirmPassword) {
        feedback.textContent = 'Passwords match';
        feedback.style.color = '#4CAF50';
    } else {
        feedback.textContent = 'Passwords do not match';
        feedback.style.color = '#ff4d4d';
    }
});

document.getElementById('changePasswordForm').addEventListener('submit', function (event) {
    const currentPassword = document.getElementById('current_password').value;
    const newPassword = document.getElementById('new_password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    // Basic validation
    if (!currentPassword || !newPassword || !confirmPassword) {
        event.preventDefault();
        alert('All fields are required');
        return false;
    }

    if (newPassword !== confirmPassword) {
        event.preventDefault();
        alert('New passwords do not match');
        return false;
    }

    // Password strength validation
    if (newPassword.length < 8) {
        event.preventDefault();
        alert('Password must be at least 8 characters long');
        return false;
    }

    return true;
});