setTimeout(function () {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.innerHTML = '';
    }
}, 3000);

function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var confirmInput = document.getElementById("confirm_password");
    var toggleButton = document.getElementById("togglePassword");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        confirmInput.type = "text";
        toggleButton.textContent = "Hide Password";
    } else {
        passwordInput.type = "password";
        confirmInput.type = "password";
        toggleButton.textContent = "Show Password";
    }
}
function submitForm() {
    const computer = document.getElementById("computer").value;
    const problemType = document.getElementById("problemType").value;
    const concern = document.getElementById("concern").value;
    const contact = document.getElementById("contact").value;

    if (computer && problemType && concern && contact) {
        // Here, you can send the data to the server for further processing (not implemented in this example).
        // You may use JavaScript fetch or an XMLHttpRequest to make an AJAX request.

        // Display a success message as a pop-up notification.
        document.getElementById("success-notification").style.display = "block";

        // Clear the form fields.
        document.getElementById("computer").value = "";
        document.getElementById("problemType").value = "";
        document.getElementById("concern").value = "";
        document.getElementById("contact").value = "";
    } else {
        // Display an error message as a pop-up notification.
        document.getElementById("error-notification").style.display = "block";
    }
}
function register() {
    window.location.href = "/register";
}

function home() {
    window.location.href = "/";
}

function login() {
    window.location.href = "/login";
}

function admin() {
    window.location.href = "/Admin";
}

function user() {
    window.location.href = "/user";
}

function UserRoles() {
    window.location.href = "/profile";
}
