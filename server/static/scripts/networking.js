// NETWORKING AND SOCKETIO CODE FOR room.html
var socket = io();

socket.on('something', function(data) {
    console.log(data);
});

socket.on('join response', function(data) {
    console.log(data);
});