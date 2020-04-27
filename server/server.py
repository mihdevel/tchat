from socket import *
from datetime import date, datetime, time
import shelve

host = '127.0.0.1'
port = 5555
chatdb = []
clients = []

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((host, port))
sockobj.listen(5)
print('Server > {}:{}'.format(host, port))

while True:
	connection, address = sockobj.accept()

	while True:
		data = connection.recv(1024).decode('utf-8')

		if not data: break
		print(address, data)

		db = shelve.open('chatdb')

		if data.find("подключёны") != -1:
			for dateTimeMsg in db:
				chatdb.append(dateTimeMsg)
			chatdb.reverse()
			for dateTimeMsg in chatdb:
				senddata = dateTimeMsg + '\n' + db[dateTimeMsg] + '\n\n'
				connection.send(senddata.encode('utf-8'))
		dateTimeNow = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
		
		senddata = dateTimeNow + '\n' + data + '\n\n'
		connection.send(senddata.encode('utf-8'))
		
		db[dateTimeNow] = data
		db.close()
	connection.close()