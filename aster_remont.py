# -*- coding: utf-8 -*-
__author__ = 'Denis'

import os
import hashlib
import binascii
from datetime import datetime

START_DIRECTORY = '/back/'
#START_DIRECTORY = '/home/da3/Beagle/потеряшкиАудиозаписи/образец/'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    #return hash_md5.hexdigest()
    return hash_md5.digest()

mp3wav_files = {}
with open('mp3wav_list.csv') as file_handler:
    for line in file_handler:
        line_list = line.split('\t')
        size = int(int(line_list[0]) / 1024)
        mp3wav_md5 = binascii.unhexlify(line_list[1])
        mp3wav_file = os.path.join(line_list[2], line_list[3])
        if mp3wav_files.get(mp3wav_md5):
            if mp3wav_files[mp3wav_md5].get(size):
                if mp3wav_file not in mp3wav_files[mp3wav_md5][size]:
                    mp3wav_files[mp3wav_md5][size].append(mp3wav_file)
            else:
                mp3wav_files[mp3wav_md5][size] = [mp3wav_file]
        else:
            mp3wav_files[mp3wav_md5] = {size: [mp3wav_file]}

mp3wav_list = open(datetime.now().strftime('%Y-%m-%d_%H-%M_') + 'mp3wav.csv', 'wt')
directories = os.listdir(START_DIRECTORY)
for directory in directories:
    if os.path.isdir(START_DIRECTORY + directory):
        files = os.listdir(START_DIRECTORY + directory)
        for file in files:
            if file.endswith('.mp3') or file.endswith('.wav'):
                wav_file_path = os.path.abspath(START_DIRECTORY + directory + '/' + file)
                if not os.path.exists(wav_file_path):
                    print wav_file_path
                else:
                    wav_size = int(os.path.getsize(wav_file_path) / 1024)
                    wav_md5 = md5(wav_file_path)
                    if mp3wav_files.get(wav_md5):
                        if mp3wav_files[wav_md5].get(wav_size):
                            if len(mp3wav_files[wav_md5][wav_size]) > 1:
                                print 'Дубли, берём только первый файл:' + str(mp3wav_files[wav_md5][wav_size])
                            mp3wav_list.write(START_DIRECTORY + directory + '/' + file + '\t'
                                              + mp3wav_files[wav_md5][wav_size][0])
mp3wav_list.close()
pass




