import socketio
import urllib.request

class DistriClient:
    global sio
    sio = socketio.Client()
    def __init__(self, url, room="", debug=False):
        self.url = url
        if room == "":
            self.room = self.generate(url)
        self.room = room
        self.debug = debug
        self._data = {} # discouraged use _
        
        sio.on('confirm', self.confirm)
        sio.on('join response', self.joinresponse)
        sio.on('updated data', self.updateddata)
        sio.connect(url)
        
        sio.emit('join', {'room': self.room})

    @property
    def data(self):
        return self._data

    def set(self, key, value):
        self.sio.emit('set', {'room':self.room, 'key':key, 'value':value})

    def confirm(self, data):
        print(data)

    def joinresponse(self, data):
        print("join response with room data: ", data)
        self._data = data

    def updateddata(self, data):
        for key in data:
            self._data[key] = data[key]
    
    def generate(self, url):
        return urllib.request.urlopen(url + "/api/generateroom").read()

