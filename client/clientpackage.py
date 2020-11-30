import socketio

# standard Python, not the asyncio version
sio = socketio.Client()
sio.connect('http://localhost:5000')

@sio.on('confirm')
def confirm(data):
    print(data)
    return

@sio.on('join response')
def joinresponse(data):
    print("join response with room data: ", data)
    tableData = data
    return

@sio.on('updated data')
def updateddata(data):
    for key in data:
        tableData[key] = data[key]
    return

tableData = {}

if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://localhost:5000')
    
    room = str(input("Enter room code: "))
    sio.emit('join', {'room': room})

    sio.emit('set', {'room': room, 'key':'From Python', 'value':'with love!'});
