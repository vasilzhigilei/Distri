function generate(){
    fetch("/api/generateroom").then(function(response) {
        response.text().then(function(text) {
            redirect(text);
        });
    });
}
function redirect(code){
    window.location.href = "/r/" + code; // redirect to new room
}
function detect_enter_keyboard(event) {
    var key_board_keycode = event.which || event.keyCode;
    if(key_board_keycode == 13){
        event.preventDefault();
        redirect(document.getElementById('code').value);
    }
}