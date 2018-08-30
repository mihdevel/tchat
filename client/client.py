from socket import *
import json
from datetime import date, datetime, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import shelve




# Var

chat = {}
my_msg = []

# Var

# chatdb = shelve.open('chatdb')
#
# for object in chatdb:
# 	chat = { object: [object[0],object[1]] }
#
# print(chat)

# Получение конфигурационных данных
with open('config.json') as json_file:
	config = json.load(json_file)
	
server_host = config['server_host']
server_port = config['server_port']
name = config['my_name']



# Соединение с сервером
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((server_host, server_port))

connection_msg = '< {} connected >'.format(name)
sockobj.send(str.encode(connection_msg))
my_msg.append(connection_msg)


# Получение шаблона чата
with open('template.txt') as file:
	template_reset = file.read()+'\n'

# Запись шаблона чата
with open('chat.txt', 'w') as file:
	file.write('<! You logged in as: ' + name + ' !>\n')
	file.write(template_reset)


# Слежка за фалом системы
class ChatHandler(FileSystemEventHandler):
	event = FileModifiedEvent('chat.txt')
	
	def on_modified(self, event):
		with open('chat.txt') as file:
			lines = file.readlines()
			try:
				text_str = lines[5].strip()
				options = lines[1].strip()
			except IndexError:
				text_str = ''
				options = ''
			
			if text_str !='' and name !='':# and != my_msg[-1]:
				sockobj.send(str.encode('{}\t\t\t> {}'.format(name, text_str)))



if __name__ == '__main__':
	
	event_handler = ChatHandler()
	observer = Observer()
	observer.schedule(event_handler, '.', recursive=False)
	observer.start()

	try:
		while True:
			data = sockobj.recv(1024)
			
			# Проверка получение данных с сервера
			if not data:
				raise KeyboardInterrup
			# continue
			
			dateTimeNow = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

			chat[dateTimeNow] = data.decode('utf-8')
			print(chat)

			# Перезагрузка шаблона + подгрузка сообщений
			with open('chat.txt', 'w') as file:
				file.write('<! You logged in as: ' + name + ' !>\n')
				file.write(template_reset)
				
				dateTimeMsgs = []
				for dateTimeMsg in chat:
					dateTimeMsgs.append(dateTimeMsg)
				
				dateTimeMsgs.reverse()
				
				for dateTimeMsg in dateTimeMsgs:
					file.write(dateTimeMsg+'\n'+chat[dateTimeMsg]+'\n\n')
			
			# print('Response:', data)
		
				# data = ast.literal_eval(data.decode('utf-8'))
				# data = json.loads(data.decode('utf-8').replace("'", '"'))
				# name = data['name']
				# msg = data['msg']
				# print(data)
				# chat[datetimeMsg] = [name,msg]
				# continue
	
	# Акуратненько все закрываем если была нажаты клавишы выхода (в linux это CTRL+C)
	except KeyboardInterrupt:
		disconnection_msg = '< {} disconnected >'.format(name)
		sockobj.send(str.encode(disconnection_msg))
		sockobj.close()
		
		my_msg.append(disconnection_msg)
		
		with open('chat.txt', 'w') as file:
			file.write('')
		observer.stop()
		# db = shelve.open('chatdb')
		# for datetime in chat:
		# 	db[datetime] = datetime
		# db.close()
	observer.join()