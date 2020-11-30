import socketio

class DistriClient:
    def __init__(url, room="", debug=False):
        self.url = url
        if room == "":
            # generate room here and set it to self.room
            pass
        self.room = room
        self.debug = debug
        self.tableData = {}
        sio = socketio.Client()
        sio.connect('http://localhost:5000')

        # join room
        sio.emit('join', {'room': self.room})

    def set(key, value):
        sio.emit('set', {'room':self.room, 'key':key, 'value':value})

    @sio.on('confirm')
    def __confirm(data):
        print(data)

    @sio.on('join response')
    def __joinresponse(data):
        print("join response with room data: ", data)
        tableData = data

    @sio.on('updated data')
    def __updateddata(data):
        for key in data:
            tableData[key] = data[key]

