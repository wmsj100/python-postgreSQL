#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 ubuntu <ubuntu@txOS>
#
# Distributed under terms of the MIT license.

"""
pgsql and oracle config
"""

pgconfig = {
    'user': 'postgres',
    'password': 'Aa123456',
    'host': '114.116.236.85',
    'port': '5432',
    'database': 'postgres',
    'schema': 'wang', # can change schema
    'table': 'p_tbm_currlog', # can change table name
}

oracle_config = {
    'user': 'SYS',
    'password': 'Oradoc_db1',
    'host': '121.36.7.55',
    'port': '1521',
    'orcl': 'ORCLCDB.localdomain',
    'owner': 'c##yan', # can change table owner
    'table': 'p_tbm_currlog', # can change table name
}
