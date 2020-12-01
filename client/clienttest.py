import clientpackage

client = clientpackage.DistriClient('http://127.0.0.1:5000', room="J8axCQ")

print(client.data)