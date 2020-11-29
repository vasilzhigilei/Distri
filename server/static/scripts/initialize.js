// INITIALIZE SOCKETIO CONNECTION WITH SERVER
socket.emit('join', {'room': document.getElementById("room").textContent});