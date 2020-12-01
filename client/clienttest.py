import clientpackage

client = clientpackage.DistriClient('http://127.0.0.1:5000', room="6fIZpg")

for i in range(50):
    if i == 25:
        client.set('1', '123')
    print(i, client.data)