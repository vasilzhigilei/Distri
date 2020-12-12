// NETWORKING AND SOCKETIO CODE FOR room.html
var socket = io();

socket.on('JOINED', function(data) {
    tableData = data;
    setTable();
    console.log("JOINED: ", data);
});

socket.on('UPDATE', function(data) {
    for (var key in data){
        tableData[key] = data[key]
    }
    setTable();
});

socket.on('ROOM_STATS', function(data) {
    document.getElementById('room_connections').innerText = data['connections'];
    document.getElementById('room_browser').innerText = data['browser'];
    document.getElementById('room_python').innerText = data['python'];
});

socket.on('SITEWIDE_STATS', function(data) {
    document.getElementById('sitewide_connections').innerText = data['connections']
    document.getElementById('sitewide_browser').innerText = data['browser']
    document.getElementById('sitewide_python').innerText = data['python']
    var d = new Date();
    var n = d.toLocaleTimeString();
    document.getElementById('sitewide_time').innerText = n; // should theoretically come from server to be accurate, but this will do
});

// helper function to check if obj is empty
function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

var tableData = {};

function setTable(){
    if(!isEmpty(tableData)){
        var tbody = "";
        for (var key in tableData){
            tbody += "<tr><th>" + key + "</th><td>" + tableData[key] + "</td></tr>";
        }
        document.getElementById("tbody").innerHTML = tbody;
    }
}