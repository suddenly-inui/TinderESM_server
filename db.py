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


def create_table_esm(engine):
    execute_sql(engine, f"drop table if exists esm")
    execute_sql(engine, "create table esm (esm_id int primary key auto_increment, title varchar(60), content varchar(60))")


def create_table_esm_activation_time(engine):
    execute_sql(engine, "drop table if exists esm_activation_time")
    execute_sql(engine, "create table esm_activation_time (id int primary key auto_increment, time time)")


def create_table_user(engine):
    execute_sql(engine, "drop table if exists user")
    execute_sql(engine, "create table user (user_id varchar(10) primary key, user_name varchar(20))")


def create_table_data(engine):
    execute_sql(engine, "drop table if exists data")
    execute_sql(engine, "create table data (idx int primary key auto_increment, user_id varchar(10), esm_id int, label varchar(10), timestamp datetime)")


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
    create_table_esm(engine)
    data = lambda title, content: {"title": title, "content": content}
    datas = [
        data("'esm1'", "'111111111111'"),
        data("'esm2'", "'222222222222'"),
        data("'esm3'", "'333333333333'"),
        data("'esm4'", "'111111111111'"),
        data("'esm5'", "'222222222222'"),
        data("'esm6'", "'333333333333'"),
        data("'esm7'", "'111111111111'"),
        data("'esm8'", "'222222222222'"),
        data("'esm9'", "'333333333333'"),
    ]
    for data in datas:
        insert_data(engine, "esm", data)

    create_table_esm_activation_time(engine)
    data = lambda time: {"time": time}
    datas = [
        data("'0:00:00'"),
        data("'2:00:00'"),
        data("'4:00:00'"),
        data("'6:00:00'"),
        data("'8:00:00'"),
        data("'10:00:00'"),
        data("'12:00:00'"),
        data("'14:00:00'"),
        data("'16:00:00'"),
        data("'18:00:00'"),
        data("'20:00:00'"),
        data("'22:00:00'"),
    ]
    for data in datas:
        insert_data(engine, "esm_activation_time", data)

    create_table_user(engine)
    data = lambda user_id, user_name: {"user_id": user_id, "user_name": user_name}
    datas = [
        data("'001'", "'inuiyuki0904'"),
        data("'002'", "'sample2'"),
        data("'003'", "'sample3'"),
        data("'004'", "'sample4'"),
    ]
    for data in datas:
        insert_data(engine, "user", data)

    create_table_data(engine)
    data = lambda user_id, esm_id, label, timestamp: {"user_id": user_id, "esm_id": esm_id, "label": label, "timestamp": timestamp}
    datas = [
        data("'001'", "1", "'right'", "'2023-09-21 14:00:00'"),
        data("'001'", "2", "'left'", "'2023-09-21 20:00:00'"),
        data("'002'", "1", "'right'", "'2023-09-21 14:00:00'"),
        data("'002'", "2", "'left'", "'2023-09-21 16:00:00'"),
        data("'003'", "1", "'right'", "'2023-09-21 14:00:00'"),
        data("'003'", "2", "'left'", "'2023-09-21 18:00:00'"),
        data("'004'", "1", "'right'", "'2023-09-21 14:00:00'"),
        data("'004'", "2", "'left'", "'2023-09-21 12:00:00'"),
    ]
    for data in datas:
        insert_data(engine, "data", data)


if __name__ == "__main__":
    engine = connect_database("TinderESM")
    create_table_esm(engine)
    create_mock(engine)


