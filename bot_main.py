from bot_handler import *
from db_handler import *
import json

def user_insert(db, user):
	id = first_name = last_name = username = ""
	if 'id' in user:
		id = user['id']
	else:
		return

	if not db.is_user_exist(id):
		if 'first_name' in user:
			first_name = user['first_name']
		if 'last_name' in user:
			last_name = user['last_name']
		if 'username' in user:
			username = user['username']
		db.insert_user(id, first_name, last_name, username)

def chat_insert(db, chat):
	id = chat_title = chat_type = ""
	if 'id' in chat:
		id = chat['id']
	else:
		return

	if not db.is_chat_exist(id):
		if 'type' in chat:
			chat_type = chat['type']
		if 'title' in chat:
			chat_title = chat['title']
		db.insert_chat(id, chat_title, chat_type)

def msg_insert(db, message, response):
	# insert_history_item(self, msg_id, user_id, chat_id, msg_type, request, response, timestamp)

	message_id = user_id = chat_id = request = ""

	if 'message_id' in message:
		message_id = message['message_id']
	if 'from' in message and 'id' in message['from']:
		user_id = message['from']['id']
	if 'chat' in message and 'id' in message['chat']:
		chat_id = message['chat']['id']
	if 'text' in message:
		request = message['text']
	if 'date' in message:
		date = message['date']

	db.insert_history_item(message_id, user_id, chat_id, "", request, response, date)


def main():
	with open('config.json') as data_file:    
		config_json = json.load(data_file)

	bot = BotHandler(config_json['token'])
	db = DataBaseHandler(config_json['db']['name'], config_json['db']['user'], config_json['db']['host'], config_json['db']['password'])
	new_offset = None

	while True:
		updates = bot.get_updates(new_offset)
		if len(updates):

			update = updates[-1]
			print json.dumps(update, indent=4, sort_keys=True)

			update_id = update['update_id']
			chat_id = chat_name = chat_text = ""
			response = ""

			if 'text' in update['message']:
				chat_text = update['message']['text']

			if 'chat' in update['message']:
				chat_id = update['message']['chat']['id']
				if 'first_name' in update['message']['chat']:
					chat_name = update['message']['chat']['first_name']

			print chat_name + ": " + chat_text

			is_send = 0
			if 'entities' in update['message'] and 'type' in update['message']['entities'][0]:
				if update['message']['entities'][0]['type'] == 'bot_command':
					if chat_text[0:4] == "/cat":
						is_send = 1
						response = bot.send_random_cat(chat_id)

			new_offset = update_id + 1

			if not is_send:
				response = bot.send_random_quote(chat_id)

			print


			if 'from' in update['message']:
				user_insert(db, update['message']['from'])

			if 'chat' in update['message']:
				chat_insert(db, update['message']['chat'])

			msg_insert(db, update['message'], response)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()