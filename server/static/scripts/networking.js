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

socket.on('STATS', function(data) {
    document.getElementById('connections').innerText = data['connections'];
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