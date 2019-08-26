# -*- coding: utf-8 -*-
__author__ = 'Denis'

import os
import hashlib
import shutil
from datetime import datetime


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    #return hash_md5.hexdigest()
    return hash_md5.digest()

def isAudio(audio):
    if audio != None:
        t = str(audio).replace('\n',' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').strip()
        t1 = t.split('/')[len(t.split(('/'))) - 1]
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

def isAudioBool(audio):
    if audio != None:
        t = str(audio).replace('\n',' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').strip()
        t1 = t.split('/')[len(t.split(('/'))) - 1]
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
with open('mp3wav_list.csv') as file_handler:
    for line in file_handler:
        line_list = line.split('\t')
        size = round(int(line_list[0]) / 10240)
        mp3wav_index = '{0:06d}'.format(round(size / 10240)) + line_list[1]
        mp3wav_file = os.path.join(line_list[2], line_list[3])
        if mp3wav_files.get(mp3wav_index):
            pass
        else:
            mp3wav_files[mp3wav_index] = mp3wav_file

if not os.path.exists('newFiles'):
    os.mkdir('newFiles')

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
drives = ['{0}:'.format(d) for d in letters if os.path.exists('{0}:'.format(d))]

all_audiofiles = []
for drive in  drives:
    walking = list(os.walk(drive))
    for root, dirs, files in walking:
        all_audiofiles += [os.path.join(root, name) for name in files if isAudioBool(name)]
audiofiles = tuple(all_audiofiles)
print('Найдено', len(audiofiles), 'аудиозаписей звонков')

for i, audiofile in enumerate(all_audiofiles):
    if i % 100:
        print('Обработано', i, 'из', len(audiofiles))
    wav_size = os.path.getsize(audiofile)
    wav_md5 = md5(audiofile)
    wav_index = '{0:06d}'.format(round(wav_size / 10240)) + wav_md5
    if mp3wav_files.get(wav_index):
        pass
    else:
        shutil.copy(audiofile, 'newFiles/' + isAudio(audiofile)[1] + audiofile[-4:])
        mp3wav_files[wav_index] = audiofile







