import socketio
import urllib.request
import time

class DistriClient:
    global sio
    sio = socketio.Client()
    def __init__(self, url, room="", debug=False):
        self.url = url
        if room == "":
            self.room = self.__generate(url)
        else:
            self.room = room
        self.DEBUG = debug
        self._data = {} # discouraged use _
        self.connected = False
        
        sio.on('JOINED', self.__joined)
        sio.on('UPDATE', self.__update)
        sio.connect(url)
        
        sio.emit('JOIN', {'room': self.room})
        for i in range(5):
            time.sleep(1)
            if(self.connected):
                return
        print("Joining room failed, closing connection")
        sio.disconnect()


    @property
    def data(self):
        return self._data

    def set(self, key, value):
        sio.emit('SET', {'room':self.room, 'key':key, 'value':value})

    def __joined(self, data):
        self.log("JOINED RESPONSE: " + str(data))
        self._data = data
        self.connected = True

    def __update(self, data):
        self.log("UPDATE RESPONSE: " + str(data))
        for key in data:
            self._data[key] = data[key]
    
    def __generate(self, url):
        return urllib.request.urlopen(url + "/api/generateroom").read().decode('UTF-8')

    def log(self, s):
        if self.DEBUG:
            print("[DISTRI] " + s)
