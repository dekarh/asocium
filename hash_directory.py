# -*- coding: utf-8 -*-
__author__ = 'Denis'

import os
import hashlib

START_DIRECTORY = '/media/da3/asteriskBeagleAl/'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    #return hash_md5.digest()

walking = list(os.walk(START_DIRECTORY))
# xlsx файлы
xlsx_files = []
xlsx_files_md5 = {}
xlsx_doubles = {}
xlsx_list = open('xlsx_list.csv', 'wt')
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
            xlsx_list.write(str(xlsx_size) + '\t' + xlsx_md5 + '\t' + xlsx_file[0] + '\t' + xlsx_file[1] + '\n')
xlsx_list.close()
for xlsx_index in xlsx_doubles:
    print(xlsx_index)
    for xlsx_file in xlsx_doubles[xlsx_index]:
        print('\t', xlsx_file)

# mp3 и wav файлы
wav_files = []
wav_files_md5 = {}
wav_doubles = {}
wav_list = open('mp3wav_list.csv', 'wt')
for root, dirs, files in walking:
    wav_files += [[root, name] for name in files if name.endswith('.mp3') or name.endswith('.wav')]
for wav_file in wav_files:
    wav_file_path = os.path.join(wav_file[0], wav_file[1])
    if not os.path.exists(wav_file_path):
        print(wav_file_path)
    else:
        wav_size = os.path.getsize(wav_file_path)
        wav_md5 = md5(wav_file_path)
        wav_index = '{0:06d}'.format(round(wav_size / 1024)) + wav_md5
        if wav_files_md5.get(wav_index):
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




