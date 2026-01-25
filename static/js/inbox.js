document.addEventListener('DOMContentLoaded', async () =>{

    try{
        const response = await fetch('/app/get_letters')
        const letters = await response.json();
        const lettersContainer = document.querySelector('#inbox-grid')
        let htmlContent = '';


        letters.forEach(element => {
            htmlContent += `<div class="envelope-card" onclick=readLetter(event) data-id="${element.id}">
        
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
                <i class="ph ph-envelope-open" style="color: #5d4037;"></i>
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
    const selectedLetter = document.querySelector(".selectedLetter");
    const paper = document.querySelector(".paper");

    if(selectedLetter != null){
        selectedLetter.classList.remove("selectedLetter");
    }    
    event.currentTarget.classList.add("selectedLetter", "read");

    paper.innerText = event.currentTarget.querySelector(".letterBody").innerText;

    const letterId = event.currentTarget.getAttribute("data-id");
    alert("Carta lida com ID: " + letterId);

    
}