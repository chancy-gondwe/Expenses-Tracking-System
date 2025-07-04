const usernameField = document.querySelector("#usernameField");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const togglePassword = document.querySelector("small.text-primary");
const submitBtn = document.querySelector(".submit-btn")


// Handle username validation
usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    const feedback = document.querySelector("#usernameFeedback");

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
                method: "POST",
                body: JSON.stringify({ username: usernameVal }),
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then((res) => res.json())
            .then((data) => {
                if (data.username_error) {
                    usernameField.classList.add("is-invalid");
                    usernameField.classList.remove("is-valid");
                    feedback.innerText = data.username_error;
                    submitBtn.Disabled = true
                } else {
                    submitBtn.removeAttribute("disabled")
                    usernameField.classList.add("is-valid");
                    usernameField.classList.remove("is-invalid");
                    feedback.innerText = "";
                }
            })
            .catch(err => {
                console.error("Username validation error:", err);
            });
    } else {
        usernameField.classList.remove("is-valid", "is-invalid");
        feedback.innerText = "";
    }
});

// Handle email validation
emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    const feedback = document.querySelector("#emailFeedback");

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
                method: "POST",
                body: JSON.stringify({ email: emailVal }),
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then((res) => res.json())
            .then((data) => {
                if (data.email_error) {

                    submitBtn.Disabled.true
                    emailField.classList.add("is-invalid");
                    emailField.classList.remove("is-valid");
                    feedback.innerText = data.email_error;
                } else {
                    submitBtn.removeAttribute("disabled");
                    emailField.classList.add("is-valid");
                    emailField.classList.remove("is-invalid");
                    feedback.innerText = "";
                }
            })
            .catch(err => {
                console.error("Email validation error:", err);
            });
    } else {
        emailField.classList.remove("is-valid", "is-invalid");
        feedback.innerText = "";
    }
});

// CSRF token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


togglePassword.addEventListener("click", () => {
    const type = passwordField.getAttribute("type");

    if (type === "password") {
        passwordField.setAttribute("type", "text");
        togglePassword.textContent = "Hide";
    } else {
        passwordField.setAttribute("type", "password");
        togglePassword.textContent = "Show";
    }
});




document.addEventListener('DOMContentLoaded', function() {
    let messageElement = document.getElementById('message');

    if (messageElement) {
        // Start fading out after 2 seconds
        setTimeout(function() {
            messageElement.classList.add('fade-out');

            // Remove the element after fade out completes
            setTimeout(function() {
                messageElement.remove();
            }, 500); // Match this with the CSS transition time
        }, 2000); // Show for 2 seconds before starting fade
    }
});