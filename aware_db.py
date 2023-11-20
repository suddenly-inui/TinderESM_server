import pandas as pd
from sqlalchemy import create_engine, text

import constants

def connect_database(database: str):
    url = f'mysql+pymysql://{constants.MYSQL_USER}:{constants.MYSQL_PASSWORD}@{constants.MYSQL_HOST}:{constants.MYSQL_PORT}/{database}?charset=utf8'
    engine = create_engine(url, echo=False)
    return engine


def execute_sql(engine, sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        conn.commit()
    return result


def insert_data(engine, table: str, data: dict):
    keys = list(data.keys())
    values = list(data.values())
    sql = f"INSERT INTO {table}({','.join(keys)}) VALUES ({','.join(values)})"
    execute_sql(engine, sql)


def create_table_users(engine):
    execute_sql(engine, f"drop table if exists users")
    execute_sql(engine, "create table users (user_id varchar(30) primary key, user_name varchar(30), password varchar(30))")


def create_table_posts(engine):
    execute_sql(engine, "drop table if exists posts")
    execute_sql(engine, "create table posts (post_id varchar(50) primary key, user_id varchar(30), content varchar(120), emotion varchar(5), timestamp datetime)")
    

def create_table_replies(engine):
    execute_sql(engine, "drop table if exists replies")
    execute_sql(engine, "create table replies (reply_id varchar(50) primary key, post_id varchar(50), user_id varchar(30), content varchar(120), timestamp datetime)")
    

def reset_table(engine, table):
    if type(table) == str:
        table = [table]
        
    for t in table:
          execute_sql(engine, f"drop table if exists {t}")


def all_tables(engine):
    r = execute_sql(engine, "show tables;")
    tables = []
    for i in r:
        for j in i:
            tables.append(j)
    return tables


def create_mock(engine):
    create_table_users(engine)
    data = lambda user_id, user_name, password: {"user_id": user_id, "user_name": user_name, "password": password}
    datas = [
        data("'aware'", "'AWARE'", "'pass'"),
    ]
    for data in datas:
        insert_data(engine, "users", data)

    create_table_posts(engine)
    data = lambda post_id, user_id, content, emotion, timestamp: {"post_id": post_id, "user_id": user_id, "content": content, "emotion": emotion, "timestamp": timestamp}
    datas = [
        data("'111111111111111111'", "'aware'", "'sample posts. \nsample new lines\nsample new lines'", "'1'", "'2023-09-21 14:00:00'"),
        data("'222222222222222222'", "'aware'", "'sample posts. \nsample new lines\nsample new lines'", "'0'", "'2023-09-21 16:00:00'"),
		data("'33333333333333333'", "'aware'", "'sample posts. \nsample new lines\nsample new lines'", "'-1'", "'2023-09-21 18:00:00'"),
		data("'444444444444444444'", "'aware'", "'sample posts. \nsample new lines\nsample new lines'", "'0'", "'2023-09-21 20:00:00'"),
		data("'555555555555555555'", "'aware'", "'sample posts. \nsample new lines\nsample new lines'", "'-1'", "'2023-09-21 22:00:00'"),
    ]
    for data in datas:
        insert_data(engine, "posts", data)
        
    create_table_replies(engine)
    data = lambda reply_id, post_id, user_id, content, timestamp: {"reply_id": reply_id, "post_id": post_id, "user_id": user_id, "content": content, "timestamp": timestamp}
    datas = [
        data("'reply11111111'", "'111111111111111111'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 14:00:00'"),
        data("'reply22222222'", "'222222222222222222'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 16:00:00'"),
		data("'reply33333333'", "'33333333333333333'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 18:00:00'"),
		data("'reply44444444'", "'444444444444444444'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 20:00:00'"),
		data("'reply55555555'", "'111111111111111111'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 22:00:00'"),
        data("'reply55555556'", "'111111111111111111'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 22:00:00'"),
		data("'reply55555554'", "'111111111111111111'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 22:00:00'"),
		data("'reply55555557'", "'111111111111111111'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 22:00:00'"),
		data("'reply55555559'", "'111111111111111111'", "'aware'", "'sample reply. \nsample new lines\nsample new lines'", "'2023-09-22 22:00:00'"),

    ]
    for data in datas:
        insert_data(engine, "replies", data)

if __name__ == "__main__":
    engine = connect_database("awareSNS")
    create_table_users(engine)
    create_table_posts(engine)
    create_mock(engine)