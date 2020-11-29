// NETWORKING AND SOCKETIO CODE FOR room.html
var socket = io({'transports': ['websocket']});

socket.on('something', function(data) {
    console.log(data);
});