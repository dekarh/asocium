# -*- coding: utf-8 -*-
__author__ = 'Denis'

import os
import hashlib
from mysql.connector import MySQLConnection

from lib import read_config

dbconfig_crm = read_config(filename='asocium.ini', section='crm')
dbconn_crm = MySQLConnection(**dbconfig_crm)
cursor_crm = dbconn_crm.cursor()
dbconfig_alone = read_config(filename='asocium.ini', section='alone')
dbconn_alone = MySQLConnection(**dbconfig_alone)
cursor_alone = dbconn_alone.cursor()
files = os.listdir('.')
is_ready = False # Пропускаем цикл пока не True
for file in files:
    if file.endswith('_mp3wav.csv'):
        with open(file) as file_handler:
            for line in file_handler:
                line_ok = False
                a_p_f = line.split('\t')[0]
                if len(a_p_f.split('/back/recup_dir.')) > 1:
                    aster_path = int(a_p_f.split('/back/recup_dir.')[1].split('/')[0])
                    aster_file = a_p_f.split('/back/recup_dir.')[1].split('/')[1]
                    if aster_file == 'f2960098456.wav':
                        is_ready = True
                        continue
                    if not is_ready:
                        continue
                    saturn_file = line.split('\t')[1].split('/')[len(line.split('\t')[1].split(('/'))) - 1]
                    saturn_file = saturn_file.strip('\n')
                    if len(saturn_file) > 16:
                        if saturn_file[13] == '-':
                            saturn_file = saturn_file[:13] + ':' + saturn_file[13 + 1:]
                        if saturn_file[16] == '-':
                            saturn_file = saturn_file[:16] + ':' + saturn_file[16 + 1:]
                    saturn_file = '%' + saturn_file
                    cursor_crm.execute("SELECT id FROM callcenter WHERE call_record LIKE %s", (saturn_file,))
                    rows = cursor_crm.fetchall()
                    if len(rows):
                        callcenter_id = rows[0][0]
                        cursor_alone.execute('INSERT INTO alone_remont(`path`, file, callcenter_id) VALUES(%s, %s, %s)',
                                             (aster_path, aster_file, callcenter_id))
                        dbconn_alone.commit()
                        line_ok = True
                if not line_ok:
                    print('Не нашли в Сатурне:', callcenter_id, aster_path, aster_file)





