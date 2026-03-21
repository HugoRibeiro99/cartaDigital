

document.getElementById('paper').addEventListener('submit', async (e) => {
    
    e.preventDefault();

    var message = document.getElementById('message').value;
    var recipient_id = document.getElementById('recipient-id').value;

    sendLetter(message, recipient_id).then(response => {
        console.log(response);
        responseTratative(response);
    });

    
});

async function sendLetter(message, recipient_id){

    const response = await fetch('/app/write_letter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_name: recipient_id, content: message, status: 'sent' })
    });

    return response;
}

async function sendToDraft(){

    var message = document.getElementById('message').value;
    var recipient_id = document.getElementById('recipient-id').value;

    const response = await fetch('/app/write_letter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_name: recipient_id, content: message})
    })
    console.log(response);
    responseTratative(response);
}

async function responseTratative(response){
    if (response.ok) {
        const data = await response.json();
        clearForm();
        sendedLetterAnimation();
    } else {
        const errorData = await response.json();
        const errorElement = document.getElementById("error-msg");
        errorElement.textContent = errorData.detail;
        errorElement.style.display = "block"
        setTimeout(() => errorElement.style.display = "none", 4000)

    }
}

function clearForm(){
    document.getElementById('message').value = '';
    document.getElementById('recipient-id').value = '';
}


function sendedLetterAnimation(){


    // criar animação com anime.js


}