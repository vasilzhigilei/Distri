// NETWORKING AND SOCKETIO CODE FOR room.html
var socket = io({'transports': ['websocket']});

socket.on('confirm', function(data) {
    console.log(data);
});

socket.on('join response', function(data) {
    tableData = data;
    setTable();
    console.log("join response with room data: ", data);
});

socket.on('updated data', function(data) {
    for (var key in data){
        tableData[key] = data[key]
    }
    setTable();
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