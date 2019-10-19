# -*- coding: utf-8 -*-
# python3 windows 7
# Собираем аудиозаписи, сигнатуры которых отсутствуют в collect.csv
__author__ = 'Denis'

import os
import sys
import hashlib
import shutil
import string
from datetime import datetime
import random


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    #return hash_md5.digest()

def isAudio(audio):
    if audio != None:
        t = str(audio).replace('\n',' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').strip()
        t1 = t.split('\\')[len(t.split(('\\'))) - 1]
        if t1.endswith('.'):
            t1 = t1[:-1]
        if t1.endswith('.mp3') or t1.endswith('.wav'):
            t1 = t1[:-4]
        if len(t1) > 30:
            if t1[2] == '.' and t1[5] == '.' and t1[10] == '_' and (t1[13] == '-' or t1[13] == '_') and \
                    (t1[16] == '-' or t1[16] == '_'):
                return ['длинный', t1]
            elif len(''.join([char for i, char in enumerate(t1) if char in string.digits and i < 26])) == 25 \
                    and t1[14] == '_':
                return ['короткий', t1]
            elif len(''.join([char for i, char in enumerate(t1) if char in string.digits and i < 30])) == 25 \
                    and t1[14] == '_' and t1[29] == '_':
                return ['короткий+СНИЛС', t1]
            else:
                return ['', audio]
        else:
            return ['', audio]
    return ['', audio]

def isAudioBool(audio):  # Добавил исключение папки newFiles !!!!
    if audio != None:
        t = str(audio).replace('\n',' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').strip()
        if t.find('newFiles') > -1:
            return False
        t1 = t.split('\\')[len(t.split(('\\'))) - 1]
        if len(t1) > 26:
            if t1[2] == '.' and t1[5] == '.' and t1[10] == '_' and (t1[13] == '-' or t1[13] == '_') and \
                    (t1[16] == '-' or t1[16] == '_'):
                return True
            elif len(''.join([char for i, char in enumerate(t1) if char in string.digits and i < 26])) == 25 \
                    and t1[14] == '_':
                return True
            elif len(''.join([char for i, char in enumerate(t1) if char in string.digits and i < 30])) == 25 \
                    and t1[14] == '_' and t1[29] == '_':
                return True
            else:
                return False
        else:
            return False
    return False


mp3wav_files = {}
if not os.path.exists('collect.csv'):
    print('Нет файла collect.csv Для его получения обратитесть в техподдержку.'
          '\n\nДля выхода из программы нажмите Enter ...')
    input()
    sys.exit()
with open('collect.csv', encoding='utf-8' ) as file_handler:
    for line in file_handler:
        line_list = line.split('\t')
        size = round(int(line_list[0]) / 1024)
        mp3wav_index = '{0:06d}'.format(size) + line_list[1]
        #mp3wav_index = line_list[1]
        mp3wav_file = os.path.join(line_list[2], line_list[3])
        if mp3wav_files.get(mp3wav_index, None):
            pass
        else:
            mp3wav_files[mp3wav_index] = mp3wav_file

if not os.path.exists('newFiles'):
    os.mkdir('newFiles')

# Добавляем те файлы, которые уже в коллекции
collected_files = os.listdir('newFiles/')
for file in collected_files:
    file_size = os.path.getsize(os.path.abspath('newFiles/' + file))
    file_md5 = md5(os.path.abspath('newFiles/' + file))
    file_index = '{0:06d}'.format(round(file_size / 1024)) + file_md5
    if not mp3wav_files.get(file_index, None):
        mp3wav_files[file_index] = os.path.abspath('newFiles/' + file)

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
drives = ['{0}:'.format(d) for d in letters if os.path.exists('{0}:'.format(d))]
print('Обнаружены диски:', drives)

all_audiofiles = []
for drive in  drives:
    walking = list(os.walk(drive + '/'))
    for root, dirs, files in walking:
        all_audiofiles += [os.path.join(root, name) for name in files if
                           (name.endswith('.mp3') or name.endswith('.wav')) and isAudioBool(os.path.join(root, name))]
audiofiles = tuple(all_audiofiles)
print('Найдено', len(audiofiles), 'аудиозаписей звонков')

for i, audiofile in enumerate(audiofiles):
    if not i % 100:
        print('Обработано', i, 'из', len(audiofiles))
    wav_size = os.path.getsize(audiofile)
    wav_md5 = md5(audiofile)
    wav_index = '{0:06d}'.format(round(wav_size / 1024)) + wav_md5
    #wav_index = wav_md5
    if mp3wav_files.get(wav_index, None):
        pass
    else:
        if not os.path.exists('newFiles/' + isAudio(audiofile)[1] + audiofile[-4:]):
            shutil.copy(audiofile, 'newFiles/' + isAudio(audiofile)[1] + audiofile[-4:])
        else:
            shutil.copy(audiofile, 'newFiles/' + str(random.randint(1,100)) + '_' + isAudio(audiofile)[1]
                        + audiofile[-4:])
        mp3wav_files[wav_index] = audiofile
print('Обработано', len(audiofiles), 'из', len(audiofiles), '\n Обработка завершена. Не забудьте скопировать в '
                            'техподдержку все файлы из папки newFiles.\n\nДля выхода из программы нажмите Enter ...')
input()
