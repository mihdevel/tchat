from socket import *
# from datetime import date, datetime, time
# import shelve

host = '127.0.0.1'
port = 5555

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((host, port))
sockobj.listen(5)
print('Server > {}:{}'.format(host, port))
clients = []

while True:
	connection, address = sockobj.accept()

	while True:
		data = connection.recv(1024)

		if not data: break
		print(address, data.decode('utf-8'))

		# db = shelve.open('chatdb')

		# if data.decode('utf-8').find("подключёны") != -1:
		# 	for obj in db:
		# 		connection.send({ obj: [obj[0],obj[1]] })

		# else:
		# 	connection.send(data)

		# 	dateTimeNow = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
		# 	chat[dateTimeNow] = data.decode('utf-8')
		# 	for datetime in chat:
		# 		db[datetime] = datetime
		# db.close()

		connection.send(data)
	connection.close()