CREATE TABLE users (
	user_id bigint PRIMARY KEY,
	first_name varchar(80),
	last_name varchar(80),
	username varchar(80)
);

CREATE TABLE chats (
	chat_id bigint PRIMARY KEY,
	chat_title varchar(80),
	chat_type varchar(20)
);

CREATE TABLE msg_history (
	msg_id bigint PRIMARY KEY,
	user_id bigint REFERENCES users(user_id),
	chat_id bigint REFERENCES chats(chat_id),
	msg_type varchar(20),
	request varchar(1000),
	response varchar(1000),
	msg_time timestamp 
);