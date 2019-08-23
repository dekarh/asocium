# -*- coding: utf-8 -*-
__author__ = 'Denis'

import os
import hashlib

START_DIRECTORY = '/home/da3/'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    #return hash_md5.digest()

xlsx_files = []
xlsx_files_md5 = {}
xlsx_doubles = {}
walking = list(os.walk(START_DIRECTORY))
# xlsx файлы
xlsx_list = open('xlsx_list.txt', 'w')
for root, dirs, files in walking:
    xlsx_files += [[root, name] for name in files if name.endswith('.xlsx') and not name.startswith('~$')]
for xlsx_file in xlsx_files:
    xlsx_file_path = os.path.join(xlsx_file[0], xlsx_file[1])
    if not os.path.exists(xlsx_file_path):
        print(xlsx_file_path)
    else:
        xlsx_size = os.path.getsize(xlsx_file_path)
        xlsx_md5 = md5(xlsx_file_path)
        xlsx_index = '{0:06d}'.format(round(xlsx_size / 1024)) + xlsx_md5
        if xlsx_files_md5.get(xlsx_index):
            if xlsx_doubles.get(xlsx_index):
                if xlsx_file_path not in xlsx_doubles[xlsx_index]:
                    xlsx_doubles[xlsx_index].append(xlsx_file_path)
            else:
                xlsx_doubles[xlsx_index] = [os.path.join(xlsx_files_md5[xlsx_index][0], xlsx_files_md5[xlsx_index][1]),
                                            xlsx_file_path]
        else:
            xlsx_files_md5[xlsx_index] = xlsx_file
for xlsx_index in xlsx_doubles:
    print(xlsx_index)
    for xlsx_file in xlsx_doubles[xlsx_index]:
        print('\t', xlsx_file)
pass




