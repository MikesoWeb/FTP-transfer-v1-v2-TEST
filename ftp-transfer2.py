from ftp_config import *
from datetime import datetime
import os
import colorama

GREEN = colorama.Fore.GREEN
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.LIGHTYELLOW_EX
BLUE = colorama.Fore.LIGHTBLUE_EX


create_dir = f'{datetime.today()}'
out_dir = r'C:\Users\z\Desktop\img'
if not os.path.exists(create_dir):
    ftp.mkd(create_dir)
ftp.cwd(create_dir)
ftp.encoding = 'utf-8'







formats = ['txt', 'mp4']


def ftp_upload(path_to_dir):
    """
    Функция для загрузки файлов на FTP-сервер
    @param path_to_dir: Путь к файлу для загрузки
    """

    start_time = datetime.now()

    transfer_files = os.listdir(path_to_dir)
    count = 0
    for path_file in transfer_files:

        full_path_file = os.path.join(path_to_dir, path_file)
        with open(full_path_file, 'rb') as fobj:
            count += 1
            print(f'...началась передача файла {BLUE}{path_file}{RESET}')

            if path_file.split('.')[-1] in formats:
                ftp.encoding = 'cp1251'

            if path_file.split('.')[-1] == 'mp3':
                ftp.encoding = 'cp1251'

            ftp.storbinary('STOR ' + path_file, fobj)

            print(
                f'Файл {GREEN}{path_file}{RESET} успешно передан за {YELLOW}{datetime.now() - start_time}{RESET} секунд')
            print()
    print('Всего файлов переданно:  {}{}{}'.format(GREEN, count, RESET))
    print('Общее время передачи файлов: {}{}{}'.format(YELLOW, datetime.now() - start_time, RESET))


ftp_upload(out_dir)

ftp.quit()
