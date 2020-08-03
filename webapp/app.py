#!/usr/bin/python3

import cx_Oracle
import psycopg2
import copy
from config import pgconfig, oracle_config

tmpObj = {
    'col_name': '',
    'pgData': set(),
    'oracleData': set()
}

def getOracle(table):
    cx_Oracle.init_oracle_client(lib_dir="/opt/instantclient_12_2")
    oracle_db = cx_Oracle.connect(oracle_config['user'], oracle_config['password'], '{host}:{port}/{orcl}'.format(host=oracle_config['host'],
        port=oracle_config['port'], orcl=oracle_config['orcl']), cx_Oracle.SYSDBA, encoding='UTF-8')
    oracle_cursor = oracle_db.cursor()
    sql = 'select "{col}" from "{user}"."{table}"'.format(col=tmpObj['col_name'], user=oracle_config['owner'], table=oracle_config['table'])
    print(sql)
    tmpObj['oracleData'] = { item[0] for item in oracle_cursor.execute(sql) }

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
    tmpObj['pgData'] = { item[0] for item in pg_cursor.fetchall() }

def compareCol():
    oracleData = copy.deepcopy(tmpObj['oracleData'])

    pgData = copy.deepcopy(tmpObj['pgData'])

    for pgItem in pgData:
        if pgItem in oracleData:
            print("current item is {}".format(pgItem))
            tmpObj['oracleData'].remove(pgItem)
            tmpObj['pgData'].remove(pgItem)

def formatPGResult():
    result = []
    result.append('\n'.join(['title: PGSQL统计数据',
        'table: {}'.format(pgconfig['table']),
        'colume: {}'.format(tmpObj['col_name']),
        'tag: 下面数据只有PGSQL有']))
    result.append('\n'.join(tmpObj['pgData']))
    with open('pgsql_result.log', 'w') as file:
        file.write('\n'.join(result))

def formatOracleResult():
    result = []
    result.append('\n'.join(['title: Oracle统计数据',
        'talbe: {}'.format(oracle_config['table']),
        'colume: {}'.format(tmpObj['col_name']),
        'tag: 下面数据只有Oracle拥有']))
    result.append('\n'.join(tmpObj['oracleData']))
    with open('oracle_result.log', 'w') as file:
        file.write('\n'.join(result))

if __name__ == '__main__':
    getPg()
    getOracle(tmpObj['col_name'])
    compareCol()
    formatPGResult()
    formatOracleResult()
