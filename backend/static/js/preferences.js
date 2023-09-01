const inputElement= document.getElementById('id_text');

inputElement.addEventListener('keydown', function(event){
    if(event.key == "Enter"){
        event.preventDefault();
    }
});