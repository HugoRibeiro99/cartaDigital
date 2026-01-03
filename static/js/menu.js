function toggleMenu() {


    const menu = document.querySelector('.menu'); 
    
    const itens = menu.querySelectorAll('li');
    

    const isOpened = itens[0].classList.contains('opened');

    const menuBtn = document.getElementById('menu-btn');
    const icon = menuBtn.querySelector('i');

    if(isOpened === true){
        classVar = "closed"
        removeVar = "opened"
        icon.className = "ph ph-dots-three-outline-vertical"
    }else{
        classVar = "opened"
        removeVar = "closed"
        icon.className = "ph ph-x-circle"
        itens[4].dataset.tooltip = "Fechar menu"
    }
    
    itens.forEach(item => {
        item.classList.toggle(classVar);
        item.classList.remove(removeVar);
    });

   
}