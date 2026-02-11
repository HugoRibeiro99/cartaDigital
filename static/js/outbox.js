const FILTER_URLS = {
    0: '/letters/inbox',              // Botão "Entregues"
    1: '/letters/outbox?status=SENT', // Botão "A caminho"
    2: '/letters/outbox?status=DRAFT' // Botão "Rascunho"
};

//     alert(checked.getAttribute("data-index"))

document.addEventListener('DOMContentLoaded', async () =>{

    checked = document.querySelector(".checked")

    try{
        const response = await fetch('/app/letters/outbox', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        } )
        const letters = await response.json();
        const lettersContainer = document.querySelector('#inbox-grid')
        let htmlContent = '';

        if(letters.length === 0 || letters.length === undefined){
            document.getElementById("empty-state").style.display = "block";
            lettersContainer.style.display = "none";
        }

        letters.forEach(element => {
            htmlContent += `<div class="envelope-card" onclick=readLetter(event) data-id="${element.uuid}">
        
            <div class="envelope-flap"></div>
            
            <div class="envelope-info">
                <div class="sender-info">
                    <i class="ph ph-user-circle"></i>
                    <span>Para: ${element.recipient_nick}</span>
                </div>
                <div class="date-info">
                    <small>${element.created_at || ''}</small>
                </div>
            </div>
            <div class="envelope-flap"></div>
            <div class="wax-seal">
               
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

function readLetter(event){
    document.querySelector(".viewer").style.display = "flex";
    document.querySelector("#inbox-grid").style.gridTemplateColumns = "1fr 1fr";

    const previousSelected = document.querySelector(".selectedLetter");
    const clickedLetter = event.currentTarget;
    const paper = document.querySelector(".paper");

    if(previousSelected != null){
        previousSelected.classList.remove("selectedLetter");
    } 
    event.currentTarget.classList.add("selectedLetter");

    paper.innerHTML = clickedLetter.querySelector(".letterBody").innerHTML;

}

function addFilter(event){

    
    checked = document.querySelector(".checked")

    checked.classList.remove("checked")

    console.log(event.currentTarget)

    event.currentTarget.classList.add("checked")


}