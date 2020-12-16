import socketio
import urllib.request
import time

class DistriClient:
    global sio
    sio = socketio.Client() # logger=True, engineio_logger=True
    def __init__(self, url, room="", debug=False):
        self.url = url
        if room == "":
            self.__room = self.__generate(url)
        else:
            self.__room = room
        self.DEBUG = debug
        self.__data = {}
        self.__room_stats = {}
        self.__sitewide_stats = {}
        self.__connected = False
        
        sio.on('JOINED', self.__joined)
        sio.on('UPDATE', self.__update)
        sio.on('ROOM_STATS', self.__update_room_stats)
        sio.on('SITEWIDE_STATS', self.__update_sitewide_stats)
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

    def get_room_stats(self):
        return self.__room_stats

    def get_sitewide_stats(self):
        return self.__sitewide_stats

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
    
    def __update_room_stats(self, data):
        self.log("ROOM STATS: " + str(data))
        for key in data:
            self.__room_stats[key] = data[key]
    
    def __update_sitewide_stats(self, data):
        self.log("SITEWIDE STATS: " + str(data))
        for key in data:
            self.__sitewide_stats[key] = data[key]

    def __generate(self, url):
        return urllib.request.urlopen(url + "/api/generateroom").read().decode('UTF-8')

    def log(self, s):
        if self.DEBUG:
            print("[DISTRI] " + s)
