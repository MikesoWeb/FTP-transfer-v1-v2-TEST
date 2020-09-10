from ftp_config import *
from datetime import datetime
import os
import colorama

GREEN = colorama.Fore.GREEN
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.LIGHTYELLOW_EX
BLUE = colorama.Fore.LIGHTBLUE_EX

create_dir = f'{datetime.today()}'
out_dir = r'C:\Users\z\Desktop\img\Русские'
# if not os.path.exists(create_dir):
#     ftp.mkd(create_dir)
ftp.mkd(f'testovaya/{create_dir}')
ftp.cwd(f'testovaya/{create_dir}')
ftp.encoding = 'utf-8'

formats = ['txt', 'mp4', 'jpg', 'docx', 'pub', 'pdf']


def ftp_upload(path_to_dir):
    """
    Функция для загрузки файлов на FTP-сервер
    @param path_to_dir: Путь к файлу для загрузки
    """

    start_time = datetime.now()

    count, count_size = 0, 0


    onlyfiles = [f for f in os.listdir(out_dir) if os.path.isfile(os.path.join(path_to_dir, f))]

    for path_file in onlyfiles:
        full_path_file = os.path.join(path_to_dir, path_file)

        with open(full_path_file, 'rb') as fobj:
            count += 1
            start_time_file = datetime.now()
            print(f'...началась передача файла {BLUE}{path_file}{RESET}')

            if path_file.split('.')[-1] in formats:
                ftp.encoding = 'cp1251'



            if path_file.split('.')[-1] == 'mp3':
                ftp.encoding = 'utf-8'
                ftp.encoding = 'cp1251'

            else:
                ftp.encoding = 'cp1251'

            ftp.storbinary('STOR ' + path_file, fobj, 1024)

            count_size += ftp.size(path_file)

        print(
            f'Файл {GREEN}{path_file}{RESET} успешно передан за {YELLOW}{datetime.now() - start_time_file}{RESET} секунд')
        print(f'Размер переданного файла: {ftp.size(path_file)} байт')

        print()
    print('Всего файлов переданно:  {}{}{}'.format(GREEN, count, RESET))
    print('Общее время передачи файлов: {}{}{}'.format(YELLOW, datetime.now() - start_time, RESET))
    print(f'Общий размер переданных файлов: {count_size // 1024000} мегабайт или {count_size} байт')

# for i in range(10):
#     ftp_upload(out_dir)

ftp_upload(out_dir)

ftp.quit()
