document.addEventListener('DOMContentLoaded', async () =>{

    try{
        const response = await fetch('/app/letters/inbox')
        const letters = await response.json();
        const lettersContainer = document.querySelector('#inbox-grid')
        let htmlContent = '';


        letters.forEach(element => {
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
        console.log(letters)

        lettersContainer.insertAdjacentHTML('beforeend', htmlContent);
    }
    catch(e) {
        console.log("Error ao carregar cartas",e)

    }

})

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


}