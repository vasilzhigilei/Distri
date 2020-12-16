// INITIALIZE SOCKETIO CONNECTION WITH SERVER
room = document.getElementById("room").value;

socket.emit('JOIN', {'room': room});

/*
Test SETs
socket.emit('SET', {'room': room, 'key':'Current i', 'value':321});
socket.emit('SET', {'room': room, 'key':'sum', 'value':'111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'});
socket.emit('SET', {'room': room, 'key':'Current i', 'value':54321});
socket.emit('SET', {'room': room, 'key':'Hello,', 'value':'World!'});
socket.emit('SET', {'room': room, 'key':'Current i', 'value':12345});
*/