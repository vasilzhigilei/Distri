import socketio

class DistriClient:
    def __init__(url, room="", debug=False):
        self.url = url
        if room == "":
            # generate room here and set it to self.room
            pass
        self.room = room
        self.debug = debug
        self._data = {} # discouraged use _
        sio = socketio.Client()
        sio.connect(url)

        # join room
        sio.emit('join', {'room': self.room})

    @property
    def data(self):
        return self._data

    def set(key, value):
        sio.emit('set', {'room':self.room, 'key':key, 'value':value})

    @sio.on('confirm')
    def __confirm(data):
        print(data)

    @sio.on('join response')
    def __joinresponse(data):
        print("join response with room data: ", data)
        self._data = data

    @sio.on('updated data')
    def __updateddata(data):
        for key in data:
            self._data[key] = data[key]

