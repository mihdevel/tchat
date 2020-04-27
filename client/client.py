import json
import shelve
from socket import *
from datetime import date, datetime, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

chat = {}

# Получение конфигурационных данных
with open('config.json') as json_file:
	config = json.load(json_file)
	
server_host = config['server_host']
server_port = config['server_port']
name = config['my_name']


# Соединение с сервером
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((server_host, server_port))

connection_msg = '< {} подключёны >'.format(name)
sockobj.send(str.encode(connection_msg))


# Получение шаблона чата
with open('template.txt') as file:
	template_reset = file.read()+'\n'

# Запись шаблона чата
with open('chat.txt', 'w') as file:
	file.write('<! Вы вошли в систему как: ' + name + ' !>\n')
	file.write(template_reset)


# Слежка за фалом системы
class ChatHandler(FileSystemEventHandler):
	event = FileModifiedEvent('chat.txt')
	
	def on_modified(self, event):
		with open('chat.txt') as file:
			lines = file.readlines()
			try:
				text_str = lines[4].strip()
			except IndexError:
				text_str = ''
			
			if text_str !='' and name !='':
				sockobj.send(str.encode('{}: {}'.format(name, text_str)))


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
				raise KeyboardInterrupt
			
			dateTimeNow = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
			chat[dateTimeNow] = data.decode('utf-8')
			print(chat[dateTimeNow])

			# Перезагрузка шаблона + подгрузка сообщений
			with open('chat.txt', 'w') as file:
				file.write('<! Вы вошли в систему как: ' + name + ' !>\n')
				file.write(template_reset)
				
				dateTimeMsgs = []
				for dateTimeMsg in chat:
					dateTimeMsgs.append(dateTimeMsg)

				dateTimeMsgs.reverse()
				for dateTimeMsg in dateTimeMsgs:
					file.write(chat[dateTimeMsg])
					# file.write(dateTimeMsg+'\n'+chat[dateTimeMsg]+'\n\n')
					# print(chat[dateTimeMsg])
	
	# Акуратненько все закрываем если была нажаты клавишы выхода (в linux это CTRL+C)
	except KeyboardInterrupt:
		disconnection_msg = '< {} отключёны >'.format(name)
		sockobj.send(str.encode(disconnection_msg))
		sockobj.close()
		with open('chat.txt', 'w') as file:
			file.write('')
		observer.stop()
	observer.join()