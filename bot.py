# -*- coding: utf-8 -*- 
from instabot import Bot 
import time 
from multiprocessing.dummy import Pool as ThreadPool 
from multiprocessing import Process 
import websocket 
import async 
ws = websocket.WebSocket() 
ws = create_connection("wss://bot-crm.ru/api/ws?key=32892839283923892832938") 
created_bots = {} 
 
 
all_messages = 0 
 
pool = ThreadPool(8) 
class inst(): 
	from instabot import Bot 
	def __init__(self, id, username, password): 
		self.id = id 
		self.username = username 
		self.password = password 
		self.users = [] 
		self.usernames = [] 
		self.fullnames = [] 
		self.messages = [] 
		self.old_messages = [] 
		self.skip_users = [] 
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
			time.sleep(2) 
 
	def first_mess(self): 
		all_mess = self.bot.get_messages() 
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
			js = {“type”: “text”, “text” : “message”, “bot”: self.id, “user”: “user_id”, “info”: {“nickname”:”username”,”name”:”fullname”}} 
			self.old_messages[user_id] = message 
			send_to_server(js) 
 
	def update(self): 
		all_mess = self.bot.get_messages() 
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
		elif js['type'] == 'media': 
			user_id = str(js['user']) 
			media = str(js['media']) 
 
 
def send_to_server(js): 
	websocket.send(js) 
 
def recv(): 
	global created_bots 
	js =  ws.recv() 
	if js['type'] == 'create_bot': 
		proc = Process(target=inst, args=(js["bot"], js["login"], js["password"])) 
		proc.start() 
   		proc.join() 
   		created_bots[js['bot']] = [js['login'], proc.name()] 
   	elif js['type'] == 'update_bot': 
 
   	elif js['type'] == 'text':  
   		created_bots[js['bot']][-1][1] 
 
 
# first_mess() 
# while True: 
# 	update() 
# 	pool.map(sends_message, users) 
# 	time.sleep(2) 