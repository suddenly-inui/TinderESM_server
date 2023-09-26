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