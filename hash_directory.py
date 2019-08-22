# -*- coding: utf-8 -*-
__author__ = 'Denis'

import os
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    #return hash_md5.hexdigest()
    return hash_md5.digest()

xlsxfiles = []
xlsxfiles_md5 = {}
xlsxdoubles = []
walking = list(os.walk('/home/da3'))
for root, dirs, files in walking:
    xlsxfiles += [[root, name] for name in files if name.endswith('.xlsx')]
for xlsxfile in xlsxfiles:
    if not os.path.exists(os.path.join(xlsxfile[0], xlsxfile[1])):
        print(xlsxfile[0], xlsxfile[1])
    else:
        a = os.stat(os.path.join(xlsxfile[0], xlsxfile[1]))
        xlsx_md5 = md5(os.path.join(xlsxfile[0], xlsxfile[1]))
        if xlsxfiles_md5.get(xlsx_md5):
            xlsxfiles_md5[xlsx_md5].append(xlsxfile)
            xlsxdoubles.append(xlsx_md5)
        else:
            xlsxfiles_md5[xlsx_md5] = [xlsxfile]
for xlsx_md5 in xlsxdoubles:
    print(xlsx_md5)
    for xlsxfile in xlsxfiles_md5[xlsx_md5]:
        print('\t', xlsxfile)
pass




