# -*- coding: utf-8 -*-
__author__ = 'Denis'

import os
import hashlib
import binascii

#START_DIRECTORY = '/back/'
START_DIRECTORY = '/home/da3/Beagle/потеряшкиАудиозаписи/образец/'

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
        size = round(int(line_list[0]) / 1024)
        mp3wav_md5 = binascii.unhexlify(line_list[1])
        mp3wav_file = os.path.join(line_list[2], line_list[3])
        if mp3wav_files.get(mp3wav_md5):
            if mp3wav_files[mp3wav_md5].get(size):
                mp3wav_files[mp3wav_md5][size].append(mp3wav_files)
            else:
                mp3wav_files[mp3wav_md5][size] = [mp3wav_files]
        else:
            mp3wav_files[mp3wav_md5] = {size: [mp3wav_files]}

directories = os.listdir(START_DIRECTORY)
for directory in directories:
    files = os.listdir(START_DIRECTORY + directory)
    for file in files:
        if file.endswith('.mp3') or file.endswith('.wav'):
            wav_file_path = os.path.abspath(START_DIRECTORY + directory + file)
            if not os.path.exists(wav_file_path):
                print(wav_file_path)
            else:
                wav_size = round(os.path.getsize(wav_file_path) / 1024)
                wav_md5 = md5(wav_file_path)
                if mp3wav_files.get(wav_md5):
                    if mp3wav_files[wav_md5].get(wav_size):




                    if wav_doubles.get(wav_index):
                        if wav_file_path not in wav_doubles[wav_index]:
                            wav_doubles[wav_index].append(wav_file_path)
                    else:
                        wav_doubles[wav_index] = [os.path.join(wav_files_md5[wav_index][0], wav_files_md5[wav_index][1]),
                                                    wav_file_path]
                else:
                    wav_files_md5[wav_index] = wav_file
                    wav_list.write(str(wav_size) + '\t' + wav_md5 + '\t' + wav_file[0] + '\t' + wav_file[1] + '\n')
        wav_list.close()
        for wav_index in wav_doubles:
            print(wav_index)
            for wav_file in wav_doubles[wav_index]:
                print('\t', wav_file)
pass




