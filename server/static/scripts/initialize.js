// INITIALIZE SOCKETIO CONNECTION WITH SERVER
room = document.getElementById("room").textContent;

socket.emit('join', {'room': room});


socket.emit('set', {'room': room, 'key':'Current i', 'value':321});