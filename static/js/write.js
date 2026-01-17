document.getElementById('paper').addEventListener('submit', async (e) => {
    alert("entrou");
    e.preventDefault();

    const message = document.getElementById('message').value;
    // var recipient_id = document.getElementById('recipient_id').value;

    var recipient_id = 0

    alert(recipient_id);

    const response = await fetch('/app/write_letter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipient_id: recipient_id, content: message })
    });

    if (response.ok) {
        const data = await response.json();
        alert(data.message);
    } else {
        const errorData = await response.json();
        const errorElement = document.getElementById('error-msg');
        errorElement.innerText = errorData.detail;
        errorElement.style.display = 'block';

    }
});