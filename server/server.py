from socket import *

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
		print(data.decode('utf-8'), address)
		connection.send(data)
	connection.close()


# while True:
# 	connection, address = sockobj.recvfrom(1024)

# 	if addr not in clients:
# 		clients.append(addr)

# 	# Обработа информации
# 	print(data.decode('utf-8'))
# 	for client in clients:
# 		server_socket.sendto(data, client)

# server_socket.close()