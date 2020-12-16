import clientpackage

client = clientpackage.DistriClient('http://127.0.0.1:5000', room="_Qoq7ry8")


print(client)

print(client.data)

print(client.get_room_stats())
import time
print(client.get_sitewide_stats())

