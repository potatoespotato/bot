# -*- coding: utf-8 -*- 
import time 
from multiprocessing.dummy import Pool as ThreadPool 
from kthread import KThread
from websocket import create_connection
from multiprocessing import Process
import json
from instabot import Bot
ws = create_connection("wss://o7.click/api/ws?key=qhs0uaf9fa")

created_bots = {} 
pool = ThreadPool(8)

'''[Bot]
[__init__(ид бота, логин, пароль) - ,
main() - бесконечное создание процессов для обновления сообщнений,
first_mess() - собирает всех пользователей и игнорит их, если после включения бота, они не пишут,
send_to_json(id) - пакует данные в json и отправляет на сервер,
update() - делает тоже самое, что и first_mess, но не игнорит пользователей,
send_to_client(js) - отправляет ответы от сервера в инстаграм]
'''
class inst(): 
	def __init__(self, id, username, password):
		print('begin', id, username, password)
		self.id = id 
		self.username = username 
		self.password = password 
		self.users = [] # id пользователей
		self.usernames = [] 
		self.fullnames = [] 
		self.messages = [] # messages и old_messages нужны для того, чтобы не спамить серверу одинаковые сообщения пользователей
		self.old_messages = [] 
		self.skip_users = [] # для игнора пользователей, которые писали до включения бота
		self.skip_messages = [] 
		self.bot = Bot() 
		self.bot.login(username = self.username, password = self.password) 
		self.pool = ThreadPool(8) 
		main(self) 
 
	def main(self): 
		first_mess(self) 
		while True: 
			update() 
			pool.map(sends_message, users) 
			time.sleep(3) 
 
	def first_mess(self): 
		all_mess = self.bot.get_messages() # парсит сообщения из деректа и собирает все данные о пользователях
		for i in range(len(all_mess['inbox']['threads'])): 
			try: 
				user_id = all_mess['inbox']['threads'][i]['items'][-1]['user_id'] 
			except: 
				pass 
			try: 
				username = all_mess['inbox']['threads'][i]['users'][-1]['username'] 
			except: 
				pass 
			try: 
				fullname = all_mess['inbox']['threads'][i]['users'][-1]['full_name'] 
			except: 
				fullname = 'None' 
			try: 
				message = all_mess['inbox']['threads'][i]['items'][-1]['text'] 
			except: 
				message = 'text' 
			if message == '': 
				message = 'text' 
			self.skip_users.append(user_id) 
			self.skip_messages.append(message) 
			self.old_messages.append(message) 
 
	def send_to_json(self, user_id): 
		message = self.messages[users.index(user_id)] 
		if message != self.old_messages[user_id]: 
			username = self.usernames[users.index(user_id)] 
			fullname = self.fullnames[users.index(user_id)] 
			js = json.dumps({'type': 'text', 'text' : message, 'bot': self.id, 'user': user_id, 'info': {'nickname':username,'name':fullname}})
			self.old_messages[user_id] = message 
			send_to_server(js) 
 
	def update(self): 
		all_mess = self.bot.get_messages() # парсит сообщения из деректа и собирает все данные о пользователях
		for i in range(len(all_mess['inbox']['threads'])): 
			try:  
				user_id = all_mess['inbox']['threads'][i]['items'][-1]['user_id'] 
			except: 
				pass 
			try: 
				username = all_mess['inbox']['threads'][i]['users'][-1]['username'] 
			except: 
				pass 
			try: 
				fullname = all_mess['inbox']['threads'][i]['users'][-1]['full_name'] 
			except: 
				fullname = 'None' 
			try: 
				message = all_mess['inbox']['threads'][i]['items'][-1]['text'] 
			except: 
				message = 'text' 
			if message == '': 
				message = 'text' 
			if str(user_id) not in str(self.users): 
				self.users.append(user_id) 
				self.messages.append(message) 
				self.usernames.append(username) 
				self.fullnames.append(fullname) 
				send_to_json(self, user_id) 
			else: 
				if self.messages[users.index(user_id)] != message: 
					self.messages[users.index(user_id)] = message 
					send_to_json(self, user_id) 
 
	def send_to_client(self, js): 
		if js['type'] == 'text': 
			user_id = str(js['user']) 
			message = str(js['text']) 
			self.bot.send_message(message, user_id) 
		elif js['type'] == 'image': 
			user_id = str(js['user']) 
			media = str(js['url'])
			self.bot.send.media(media, user_id)
 
'''[Server]
[send_to_server(json) - отправляет данные от бота серверу, 
recv - прослушивание порта на новые сообщения,
create_bot(json) - при получении команды create_bot создает тред для нового бота,
update_bot(json) - перезапускает тред бота с новыми данными,
pings() - отправляет пинг-фреймы серверу, чтобы соединение не прервалось]
'''
def send_to_server(js):
	ws.send(js)

def recvs():
	while True:
		global created_bots
		result =  ws.recv()
		print(result)
		if result and result != 'PONG':
			js = json.loads(result)
			print(js)
			if js.get('error') == None:
				if js['type'] == 'create_bot':
					create_bot(js)
				elif js['type'] == 'update_bot':
					update_bot(js)
				elif js['type'] == 'text' or js['type'] == 'media':
					created_bots[js['bot']][2].send_to_client(js)
		print(created_bots)

def create_bot(js):
	global created_bots
	if created_bots.get(js["bot"]) == None:
		proc = Process(target=inst, args=(js["bot"], js["login"], js["pass"])) 
		proc.start()
		created_bots[js['bot']] = [js['login'], proc.name(), proc]

def update_bot(js):
	global created_bots
	try:
		proc.terminate()
		proc = Process(target=inst, args=(js["bot"], js["login"], js["pass"])) 
		proc.start()
		created_bots[js['bot']] = [js['login'], proc]
	except:
		proc = Process(target=inst, args=(js["bot"], js["login"], js["pass"])) 
		proc.start()
		created_bots[js['bot']] = [js['login'], proc]

def pings():
	while True:
		print('PING')
		ws.send('PING')
		time.sleep(15)

pig = KThread(target=pings)
rec = KThread(target=recvs)
pig.start()
rec.start()
