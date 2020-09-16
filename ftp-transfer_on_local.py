import time

from ftp_config import ftp, formats
from datetime import datetime
import os
from ftp_config import GREEN,YELLOW,BLUE,RESET
from pathlib import Path, PurePath

ftp.cwd('test')
ftp.encoding='cp1251'

filenames = ftp.nlst()

count = 0
count_size = 0
start_time = datetime.now()

txt_list = []
binary_list = []
path_local = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

for filename in filenames:
    # заменил os.path.join
    file = Path(path_local, filename)
    if not os.path.exists(path_local):
        os.mkdir(path_local)
    else:

        with open(file, 'wb') as f:
            count+=1

            # заменил file.split('.')[-1]
            if  PurePath(filename).suffix in formats:

                ftp.retrlines('RETR ' + filename, f.write)
                txt_list.append(filename)
                print(f'Файл текстовый, передаю в режиме RETRLINES')

            else:

                ftp.retrbinary('RETR ' + filename, f.write, 4096)
                binary_list.append(filename)
                print(f'Файл бинарный, передаю в режиме RETRBINARY')

            count_size += ftp.size(filename)
            print(
                f'Файл {GREEN}{filename}{RESET} успешно передан за {YELLOW}{datetime.now() - start_time}{RESET} секунд')
            print(f'Размер переданного файла: {ftp.size(filename)} байт')
            print()

# f1 = open('txt_list.txt', 'w')
# for k in txt_list:
#     file_txt = f1.write(k)
# f1.close()
# f2 = open('binary_list.txt', 'w')
# for v in binary_list:
#     file_binary = f2.write(v)
print('Всего файлов переданно:  {}{}{}'.format(GREEN, count, RESET))
print('Общее время передачи файлов: {}{}{}'.format(YELLOW, datetime.now() - start_time, RESET))
print(f'Общий размер переданных файлов: {count_size//1024000} мегабайт или {count_size} байт')
ftp.quit()