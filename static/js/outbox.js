document.addEventListener('DOMContentLoaded', async () =>{

    try{
        const response = await fetch('/app/letters/outbox')
        const letters = await response.json();
        console.log(letters)
        const lettersContainer = document.querySelector('#inbox-grid')
        let htmlContent = '';


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