import socketio
import urllib.request
import time

class DistriClient:
    global sio
    sio = socketio.Client()
    def __init__(self, url, room="", debug=False):
        self.url = url
        if room == "":
            self.__room = self.__generate(url)
        else:
            self.__room = room
        self.DEBUG = debug
        self.__data = {}
        self.__connected = False
        
        sio.on('JOINED', self.__joined)
        sio.on('UPDATE', self.__update)
        sio.connect(url)
        
        sio.emit('JOIN', {'room': self.__room})
        for i in range(5):
            time.sleep(1)
            if(self.__connected):
                return
        print("Joining room failed, closing connection")
        sio.disconnect()

    def __str__(self):
        return self.__room + " " + str(self.__data)

    @property
    def data(self):
        return self.__data

    def get_room(self):
        return self.__room

    def set(self, key, value):
        sio.emit('SET', {'room':self.__room, 'key':key, 'value':value})

    def __joined(self, data):
        self.log("JOINED RESPONSE: " + str(data))
        self.__data = data
        self.__connected = True

    def __update(self, data):
        self.log("UPDATE RESPONSE: " + str(data))
        for key in data:
            self.__data[key] = data[key]
    
    def __generate(self, url):
        return urllib.request.urlopen(url + "/api/generateroom").read().decode('UTF-8')

    def log(self, s):
        if self.DEBUG:
            print("[DISTRI] " + s)
