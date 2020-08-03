#!/usr/bin/python3

import cx_Oracle
import psycopg2

cx_Oracle.init_oracle_client(lib_dir="/opt/instantclient_12_2")
oracle_db = cx_Oracle.connect('JIAYAN', 'jiayan', '121.36.7.55:1522/orcl', encoding='UTF-8')
oracle_cursor = oracle_db.cursor()
pg_db = psycopg2.connect(database='test1', user='postgres', password='Aa123456', host='114.116.236.85', port='5432')
pg_cursor = pg_db.cursot()

