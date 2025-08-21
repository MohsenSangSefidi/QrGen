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
});
