document.getElementById('paper').addEventListener('submit', async (e) => {
    
    e.preventDefault();

    const message = document.getElementById('message').value;
    var recipient_id = document.getElementById('recipient-id').value;

    console.log(message)

    const response = await fetch('/app/write_letter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_name: recipient_id, content: message })
    });

    if (response.ok) {
        const data = await response.json();
    } else {
        const errorData = await response.json();
        const errorElement = document.getElementById("error-msg");
        errorElement.textContent = errorData.detail;
        errorElement.style.display = "block"
        setTimeout(() => errorElement.style.display = "none", 4000)

    }
});