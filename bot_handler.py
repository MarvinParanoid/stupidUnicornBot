import requests  
import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.oops_message = "Sorry, i couldn't do it :( But i am still pretty, yeah? :3"

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp 

    def send_photo(self, chat_id, photo):
        params = {'chat_id': chat_id, 'photo': photo}
        method = 'sendPhoto'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_oops_message(self, chat_id):
        print "Something goes wrong"
        self.send_message(chat_id, self.oops_message)

    def get_chat_id(update):  
        chat_id = update['message']['chat']['id']
        return chat_id

    def send_random_cat(self, chat_id):
        try:
            resp = requests.post("http://aws.random.cat/meow").json()
            self.send_photo(chat_id, resp['file'])
        except:
            self.send_oops_message(chat_id)
            return self.oops_message

    def send_random_quote(self, chat_id):
        try:
            resp = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=ru").json()
            s =  resp['quoteText'] + ' ' + resp['quoteAuthor']
            self.send_message(chat_id, s)
            print s
            return s
        except:
            self.send_oops_message(chat_id)
            return self.oops_message
