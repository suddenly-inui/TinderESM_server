from fastapi import FastAPI
import logging
import datetime
import pytz

import db

logger = logging.getLogger(__name__)
engine = db.connect_database("TinderESM")
timezone = pytz.timezone('Asia/Tokyo')
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.get("/send_label")
def read_root(user_id: str, esm_id: int, label: str):
    now = datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
    db.execute_sql(engine, f"insert into data(user_id, esm_id, label, timestamp) values('{user_id}', {esm_id}, '{label}', '{now}')")
    return {
                "label": label,
                "success": True
            }


@app.get("/send_user")
def send_user(user_id: str, user_name: str):
    success = True
    try:
        db.execute_sql(engine, f"insert into user(user_id, user_name) values('{user_id}', '{user_name}')")
    except:
        success = False

    return {
        "user_id": user_id,
        "user_name": user_name,
        "success": success
    }



@app.get("/esm_active")
def esm_time():
    active = False

    # 現在時刻
    now = datetime.datetime.now(timezone)
    # timedeltaの元となる時刻
    baseTime = now.replace(hour=0, minute=0, second=0)
    # databaseからesmの起動時間をフェッチ(->timedelta)
    esm_time = db.execute_sql(engine, "select * from esm_activation_time")
    for time in esm_time:
        due = baseTime + time[1]
        if due <= now <= due+datetime.timedelta(minutes=10):
            active = True
    return {
        "active": active
    }


@app.get("/esm_time")
def esm_time():
    # databaseからesmの起動時間をフェッチ(->timedelta)
    esm_time = db.execute_sql(engine, "select * from esm_activation_time").fetchall()
    esm_time_list = [time[1] for time in esm_time]
    print(esm_time_list)
    return esm_time_list


@app.get("/esm")
def esm():
    esm = db.execute_sql(engine, "select * from esm").fetchall()
    esm_list = [{'esm_id': item[0], 'title': item[1], 'content': item[2]} for item in esm]
    
    return esm_list


# 以下、awareSNS

@app.get("/aware/posts")
def posts():
    engine = db.connect_database("awareSNS")
    posts = db.execute_sql(engine, "SELECT posts.*, users.user_name, COUNT(replies.reply_id) AS reply_count FROM posts LEFT JOIN replies ON posts.post_id = replies.post_id LEFT JOIN users ON posts.user_id = users.user_id GROUP BY posts.post_id ORDER BY posts.timestamp DESC LIMIT 100;").fetchall()
    posts = [{'post_id': item[0], 'user_id': item[1], 'user_name': item[5], 'content': item[2], "emotion": item[3], "timestamp": item[4], "reply_count": item[6]} for item in posts]

    return posts


@app.get("/aware/send_post")
def send_post(user_id: str, content: str, emotion: str):
    engine = db.connect_database("awareSNS")
    success = True
    try:
        current_datetime = datetime.datetime.now(timezone)
        timestamp_milliseconds = int(current_datetime.timestamp() * 1000)
        post_id = f"{user_id}{timestamp_milliseconds}"
        db.execute_sql(engine, f"insert into posts(post_id, user_id, content, emotion, timestamp) values('{post_id}', '{user_id}', '{content}', '{emotion}', '{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}')")
    except Exception as e:
        success = False
        print(e)

    return{
        "success": success
    }


@app.get("/aware/get_emotion")
def get_emotion(user_id):
    return {
        "emotion": "0.5"
    }


@app.get("/aware/user")
def posts(user_id: str):
    engine = db.connect_database("awareSNS")
    user = db.execute_sql(engine, f"SELECT * FROM users where user_id = '{user_id}'").fetchone()
    if user is not None:
        id = user[0]
        name = user[1]
    else:
        id = ""
        name = ""


    return {
        "user_id": id,
        "user_name": name
    }


@app.get("/aware/send_reply")
def send_reply(post_id: str, user_id: str, content: str):
    engine = db.connect_database("awareSNS")
    success = True
    try:
        current_datetime = datetime.datetime.now(timezone)
        timestamp_milliseconds = int(current_datetime.timestamp() * 1000)
        reply_id = f"reply{user_id}{timestamp_milliseconds}"
        db.execute_sql(engine, f"insert into replies(reply_id, post_id, user_id, content, timestamp) values('{reply_id}', '{post_id}', '{user_id}', '{content}', '{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}')")
    except Exception as e:
        success = False
        print(e)

    return{
        "success": success
    }


@app.get("/aware/replies")
def replies(post_id: str):
    engine = db.connect_database("awareSNS")
    replies = db.execute_sql(engine, f"SELECT * FROM replies LEFT JOIN users ON replies.user_id = users.user_id WHERE post_id = '{post_id}'  ORDER BY timestamp DESC LIMIT 100;").fetchall()
    replies = [{'reply_id': item[0], 'post_id': item[1], 'user_id': item[2], 'user_name': item[6], 'content': item[3], "timestamp": item[4]} for item in replies]

    return replies


@app.get("/aware/sign_in")
def sign_in(user_id: str, user_name: str, password: str):
    engine = db.connect_database("awareSNS")
    success = True
    try:
        db.execute_sql(engine, f"insert into users(user_id, user_name, password) values('{user_id}', '{user_name}', '{password}')")
    except Exception as e:
        success = False
        print(e)

    return{
        "success": success
    }


@app.get("/aware/log_in")
def log_in(user_id: str, password: str):
    engine = db.connect_database("awareSNS")
    success = True
    try:
        user = db.execute_sql(engine, f"SELECT * FROM users where user_id = '{user_id}'").fetchone()
        if user is not None:
            success = (user[2] == password)
        else:
            success = False
    except Exception as e:
        success = False

    return{
        "success": success
    }


@app.get("/aware/is_user_registered")
def is_user_registered(user_id: str):
    engine = db.connect_database("awareSNS")
    success = True
    try:
        user = db.execute_sql(engine, f"select * from users where user_id = '{user_id}';").fetchall()
        if not user:
            success = False
    except Exception as e:
        success = False
        print(e)

    return{
        "success": success
    }