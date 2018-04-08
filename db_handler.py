import psycopg2
import datetime

class DataBaseHandler:

    def __init__(self, dbname, user, host, password):
        self.conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close();
        self.conn.close();

    def get_datetime_from_timestamp(self, timestamp):
        return datetime.datetime.utcfromtimestamp((int)(timestamp)).strftime('%Y-%m-%d %H:%M:%S');

    def insert_user(self, user_id, first_name, last_name, username):
        self.cur.execute("INSERT INTO users VALUES(%s, %s, %s, %s);", (user_id, first_name, last_name, username,))
        self.conn.commit()

    def foo(self):
        self.cur.execute("SELECT * FROM users;")
        text = self.cur.fetchall()
        print(text)

    def insert_history_item(self, msg_id, user_id, chat_id, msg_type, request, response, timestamp):
        datetime = self.get_datetime_from_timestamp(timestamp)
        self.cur.execute("INSERT INTO msg_history VALUES(%s, %s, %s, %s, %s, %s, %s);", (msg_id, user_id, chat_id, msg_type, request, response, datetime,))
        self.conn.commit()

    def insert_chat(self, chat_id, chat_title, chat_type):
        self.cur.execute("INSERT INTO chats VALUES(%s, %s, %s);", (chat_id, chat_title, chat_type,))
        self.conn.commit()


    def is_user_exist(self, user_id):
        self.cur.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
        return len(self.cur.fetchall())

    def is_chat_exist(self, chat_id):
        self.cur.execute("SELECT * FROM chats WHERE chat_id = %s;", (chat_id,))
        return len(self.cur.fetchall())
