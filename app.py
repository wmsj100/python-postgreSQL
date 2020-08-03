#!/usr/bin/python3

import cx_Oracle
import psycopg2
import json

pgconfig = {
    'user': 'postgres',
    'password': 'Aa123456',
    'host': '114.116.236.85',
    'port': '5432',
    'database': 'postgres',
    'schema': 'wang',
    'table': 'p_tbm_currlog',
}

oracle_config = {
    'user': 'SYS',
    'password': 'Oradoc_db1',
    'host': '121.36.7.55',
    'port': '1521',
    'orcl': 'ORCLCDB.localdomain',
    'owner': 'c##yan',
    'table': 'p_tbm_currlog',
}

tmpObj = {
    'col_name': '',
    'pgData': [],
    'oracleData': [],
}

def getOracle(table):
    cx_Oracle.init_oracle_client(lib_dir="/opt/instantclient_12_2")
    oracle_db = cx_Oracle.connect(oracle_config['user'], oracle_config['password'], '{host}:{port}/{orcl}'.format(host=oracle_config['host'],
        port=oracle_config['port'], orcl=oracle_config['orcl']), cx_Oracle.SYSDBA, encoding='UTF-8')
    oracle_cursor = oracle_db.cursor()
    sql = 'select "{col}" from "{user}"."{table}"'.format(col=tmpObj['col_name'], user=oracle_config['owner'], table=oracle_config['table'])
    print(sql)
    tmpObj['oracleData'] = [ item[0] for item in oracle_cursor.execute(sql) ]
#    oracle_cursor.execute('select * from {user}.{table}')

def getPg():
    pg_db = psycopg2.connect(database=pgconfig['database'], user=pgconfig['user'], password=pgconfig['password'], host=pgconfig['host'], port=pgconfig['port'])
    pg_cursor = pg_db.cursor()
    sql = 'SET search_path TO {schema}'.format(schema = pgconfig['schema'])
    print(sql)
    pg_cursor.execute(sql)
    sql = "select column_name from information_schema.columns where table_name='{table}'".format(table = pgconfig['table'])
    print(sql)
    pg_cursor.execute(sql)
    first_col = [ item[0] for item in pg_cursor.fetchall() ][0]
    print('first_col is {}'.format(first_col))
    tmpObj['col_name'] = first_col
    sql = "select {col} from {table}".format(col=first_col, table=pgconfig['table'])
    print(sql)
    pg_cursor.execute(sql)
    tmpObj['pgData'] = [ item[0] for item in pg_cursor.fetchall() ]

def writeResult():
    print(json.dumps(tmpObj))
    with open('data.log', 'w') as file:
        file.write(json.dumps(tmpObj))

if __name__ == '__main__':
    getPg()
    getOracle(tmpObj['col_name'])
    writeResult()
