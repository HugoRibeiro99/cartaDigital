document.addEventListener("DOMContentLoaded", () => {
    
    const userName = localStorage.getItem("userName");
    const userNameHTML = document.querySelector(".user-name");

    if (userName) {
        userNameHTML.textContent = userName;
    }
    
});


function dropDown() {

    var dropdown = document.getElementsByClassName("dropdown-content")[0];

    if (dropdown.style.display === "flex") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "flex";
    }
}

function logout(){

    fetch('/auth/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            console.log(response);
            window.location.href = response.redirect_url || 'auth/login';
        } else {
            console.error('Logout failed');
        }
    })
    .catch(error => console.error('Error:', error));
}