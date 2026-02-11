var globalLetters = [];

document.addEventListener('DOMContentLoaded', async () =>{

    try{
        const response = await fetch('/app/letters/inbox')
        const letters = await response.json();
        globalLetters = letters;
        LettersRender(letters);

    }
    catch(e) {
        console.log("Error ao carregar cartas",e)

    }

})


function LettersRender(letters, filterIndex = 0){

    const unreadLetters = letters.filter(letter => !letter.read);
    const readLetters = letters.filter(letter => letter.read);
    let filteredLetters = [];

    if(filterIndex == 0){
        filteredLetters = letters;
    }else if(filterIndex == 1){
        filteredLetters = unreadLetters;
    }else{
        filteredLetters = readLetters;
    }

    const lettersContainer = document.querySelector('#inbox-grid')
    lettersContainer.innerHTML = '';
    let htmlContent = '';

    filteredLetters.forEach(element => {
        htmlContent += `<div class="envelope-card ${element.read ? "read": null}" onclick=readLetter(event) data-id="${element.uuid}" data-read="${element.read}">
    
        <div class="envelope-flap"></div>
        
        <div class="envelope-info">
            <div class="sender-info">
                <i class="ph ph-user-circle"></i>
                <span>De: ${element.sender_nick}</span>
            </div>
            <div class="date-info">
                <small>${element.created_at || ''}</small>
            </div>
        </div>
        <div class="envelope-flap"></div>
        <div class="wax-seal">
            ${element.read ? '<i class="ph ph-envelope-open"></i>' : '<i class="ph ph-seal-check"></i>'}
        </div>
        <div class="letterBody" >${element.content}</div>
    </div>`
    });

    lettersContainer.insertAdjacentHTML('beforeend', htmlContent);

}

async function readLetter(event){
    
    document.querySelector(".viewer").style.display = "flex";
    document.querySelector("#inbox-grid").style.gridTemplateColumns = "1fr 1fr";

    const previousSelected = document.querySelector(".selectedLetter");
    const clickedLetter = event.currentTarget;
    const paper = document.querySelector(".paper");


    if(previousSelected != null){
        previousSelected.classList.remove("selectedLetter");
    }    
    event.currentTarget.classList.add("selectedLetter", "read");

    const maxSeal = clickedLetter.querySelector(".ph-seal-check");
    
    paper.innerHTML = clickedLetter.querySelector(".letterBody").innerHTML;

    if(clickedLetter.getAttribute("data-read") == "false"){

        const letterId = event.currentTarget.getAttribute("data-id");

        const response = await fetch('/app/mark_as_read', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({uuid: letterId, is_read: true})
        });

        if(response.ok){
            if(maxSeal){
                maxSeal.classList.replace("ph-seal-check", "ph-envelope-open");
                clickedLetter.setAttribute("data-read", "true");
                globalLetters.find(letter => letter.uuid == letterId).read = true;
                console.log(globalLetters);
            }
        }else{
            console.error("Erro ao marcar como lida");
        }
    }
}

function addFilter(event){

    
    checked = document.querySelector(".checked")

    checked.classList.remove("checked")

    console.log(event.currentTarget)

    event.currentTarget.classList.add("checked")

    let filterIndex = event.currentTarget.getAttribute("data-index");

    if(filterIndex == "0" ){
        LettersRender(globalLetters, 0);
    }else if(filterIndex == "1"){
        LettersRender(globalLetters, 1);
    }else{
        LettersRender(globalLetters, 2);
    }


}