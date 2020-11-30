import socketio

# standard Python, not the asyncio version
sio = socketio.Client()
sio.connect('http://localhost:5000')

@sio.on('confirm')
def confirm(data):
    print(data)

@sio.on('join response')
def joinresponse(data):
    print("join response with room data: ", data)
    tableData = data

@sio.on('updated data')
def updateddata(data):
    for key in data:
        tableData[key] = data[key]

room = str(input("Enter room code: "))
sio.emit('join', {'room': room})

sio.emit('set', {'room': room, 'key':'From Python', 'value':'with love!'});

tableData = {}