document.addEventListener('DOMContentLoaded', function () {
    // Tab switching
    const loginTab = document.getElementById('loginTab');
    const signupTab = document.getElementById('signupTab');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const switchToSignup = document.getElementById('switchToSignup');
    const switchToLogin = document.getElementById('switchToLogin');

    // Function to switch tabs
    function switchToLoginTab() {
        loginTab.classList.add('active');
        signupTab.classList.remove('active');
        loginForm.classList.add('active');
        signupForm.classList.remove('active');
    }

    function switchToSignupTab() {
        loginTab.classList.remove('active');
        signupTab.classList.add('active');
        loginForm.classList.remove('active');
        signupForm.classList.add('active');
    }

    // Event listeners for tabs
    loginTab.addEventListener('click', switchToLoginTab);
    signupTab.addEventListener('click', switchToSignupTab);

    // Event listeners for switch links
    switchToLogin.addEventListener('click', function (e) {
        e.preventDefault();
        switchToLoginTab();
    });

    switchToSignup.addEventListener('click', function (e) {
        e.preventDefault();
        switchToSignupTab();
    });

    const toast = document.getElementById('toast');

    // Toast notification
    function showToast(message, type) {
        toast.textContent = message;
        toast.className = 'toast show';

        // Set background color based on type
        switch (type) {
            case 'success':
                toast.style.backgroundColor = '#4cc9f0';
                break;
            case 'error':
                toast.style.backgroundColor = '#f72585';
                break;
            case 'info':
                toast.style.backgroundColor = '#4361ee';
                break;
            default:
                toast.style.backgroundColor = '#1a1a2e';
        }

        // Hide after 3 seconds
        setTimeout(function () {
            toast.className = 'toast';
        }, 3000);
    }

    // Check if we have a simulated Django message
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('created');

    if (message) {
        showToast('Account created successfully!', 'success');
    }
});
