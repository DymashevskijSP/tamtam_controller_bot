import psycopg2
import time

cur = None
conn = None
table_name = "mentions_info034"


def connect():
    global conn, cur
    conn = psycopg2.connect("dbname=mydb user=megaserg01 password=123")
    conn.autocommit = True
    cur = conn.cursor()


def create_spider_db():
    cur.execute(
        f"CREATE TABLE {table_name} (channel_id bigint PRIMARY KEY NOT NULL, last_checked_message bigint , first_checked_message bigint , mentions integer);")


def add_channel(channel_id, time):
    try:
        cur.execute(
            f"INSERT INTO {table_name} (channel_id, last_checked_message, first_checked_message, mentions) values (%s, %s, %s, %s);",
            (channel_id, time, time, 1))
    except:
        pass


def add_mention(channel_id):
    cur.execute("SELECT mentions from {} where channel_id={}".format(table_name, channel_id))
    current_mentions = cur.fetchone()
    try:
        cur.execute(
            "UPDATE {} SET mentions = {} where channel_id={};".format(table_name, int(current_mentions[0]) + 1,
                                                                      channel_id))
    except:
        pass


def get_last_time(channel_id):
    cur.execute(f"SELECT  last_checked_message from {table_name} where channel_id={channel_id}")
    return cur.fetchone()


def get_first_time(channel_id):
    cur.execute(f"SELECT  first_checked_message from {table_name} where channel_id={channel_id}")
    return cur.fetchone()


def set_last_time(channel_id, time):
    cur.execute("UPDATE {} SET last_checked_message = {} where channel_id={};".format(table_name, time, channel_id))
    conn.commit()


def set_first_time(channel_id, time):
    cur.execute("UPDATE {} SET first_checked_message = {} where channel_id={};".format(table_name, time, channel_id))
    conn.commit()


def disconnect():
    conn.commit()
    cur.close()
    conn.close()


def get_all_chats():
    cur.execute(f"SELECT channel_id from {table_name}")
    res = cur.fetchone()
    if (res is not None):
        return res
    return []


def get_mentions(chat_id):
    cur.execute("SELECT mentions from {} where channel_id={}".format(table_name, chat_id))


connect()
create_spider_db()