from bot_handler import *
import json

def main():

	token = ""
	with open('config.json') as data_file:    
		token = json.load(data_file)['token']


	bot = BotHandler(token)
	new_offset = None

	while True:
		updates = bot.get_updates(new_offset)
		if len(updates):

			last_update = updates[-1]
			print json.dumps(last_update, indent=4, sort_keys=True)

			last_update_id = last_update['update_id']
			last_chat_id = ""
			last_chat_name = ""
			last_chat_text = ""

			print last_chat_name
			print last_chat_text
			print

			if 'text' in last_update['message']:
				last_chat_text = last_update['message']['text']

			if 'chat' in last_update['message']:
				last_chat_id = last_update['message']['chat']['id']
				if 'first_name' in last_update['message']['chat']:
					last_chat_name = last_update['message']['chat']['first_name']


			is_send = 0
			if 'entities' in last_update['message']:
				print '1'
				if 'type' in last_update['message']['entities'][0]:
					print '2'
					if last_update['message']['entities'][0]['type'] == 'bot_command':
						print '3'
						if last_chat_text[0:4] == "/cat":
							print '4'
							is_send = 1
							bot.send_random_cat(last_chat_id)


			new_offset = last_update_id + 1

			if not is_send:
				bot.send_random_quote(last_chat_id)



if __name__ == '__main__':
	main()