from ftp_config import *
from datetime import datetime
import os
import colorama

GREEN = colorama.Fore.GREEN
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.LIGHTYELLOW_EX
BLUE = colorama.Fore.LIGHTBLUE_EX

formats = ['txt', 'mp4', 'jpg']
ftp.cwd('testovaya/2020-09-10 18:28:07.973063')
ftp.encoding='cp1251'

filenames = ftp.nlst()
count = 0
count_size = 0
start_time = datetime.now()
for filename in filenames:
    file = os.path.join('test', filename)

    with open(file, 'wb') as f:
        count+=1


        # if file.split('.')[-1] in formats:
        # ftp.encoding='utf-8'
        ftp.retrbinary('RETR ' + filename, f.write)


        # else:
        #     # ftp.encoding='1251'
        #     ftp.retrbinary('RETR ' + filename, f.write)
        count_size += ftp.size(filename)
        print(
            f'Файл {GREEN}{filename}{RESET} успешно передан за {YELLOW}{datetime.now() - start_time}{RESET} секунд')
        print(f'Размер переданного файла: {ftp.size(filename)} байт')
        print()
print('Всего файлов переданно:  {}{}{}'.format(GREEN, count, RESET))
print('Общее время передачи файлов: {}{}{}'.format(YELLOW, datetime.now() - start_time, RESET))
print(f'Общий размер переданных файлов: {count_size//1000000} мегабайт или {count_size} байт')
ftp.quit()