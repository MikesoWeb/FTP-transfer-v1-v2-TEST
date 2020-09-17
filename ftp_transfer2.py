import time
from zipfile import ZipFile
import shutil

from ftp_config import ftp, formats
from datetime import datetime
import os
from pathlib import PurePath, Path
from ftp_config import GREEN, YELLOW, BLUE, RESET

create_dir = f'{datetime.today().strftime("%Y-%m-%d-%H-%M-%S")}'

# Указываем откуда будем брать данные дял передачи
out_dir = 'test'

ftp.cwd('test')
ftp.mkd(create_dir)

ftp.cwd(f'{create_dir}')
ftp.encoding = 'cp1251'


def ftp_upload(path_to_dir):
    """
    Функция для загрузки файлов на FTP-сервер
    @param path_to_dir: Путь к файлу для загрузки
    """

    txt_list = []
    binary_list = []
    start_time = datetime.now()
    count_txt = 0
    count_binary = 0
    count_txt_size = 0
    count_binary_size = 0
    count, count_size = 0, 0

    # Собираем файлы из папки
    list_local_dir = os.listdir(out_dir)
    # заменил os.path.join
    # заменил listdir
    onlyfiles = [f for f in list_local_dir if os.path.isfile(Path(path_to_dir, f))]

    for path_file in onlyfiles:
        # заменил os.path.join
        full_path_file = Path(path_to_dir, path_file)
        # проверка если папка, то вычесть из списка общего
        if Path(full_path_file).is_dir():
            onlyfiles = len(onlyfiles) - 1

        else:
            count += 1

        # создается архив
        # z = ZipFile(f'{create_dir}.zip', 'w')
        # for root, dirs, files in os.walk(out_dir):
        #     for file in files:
        #         z.write(os.path.join(root, file))
        # z.close()

        shutil.make_archive(f'{create_dir}', 'zip', out_dir)


        with open(full_path_file, 'rb') as fobj:
            time_transfer_txt = datetime.today().strftime('%d-%m-%Y %H-%M-%S')


            start_time_file = datetime.now()
            print(f'...началась передача файла {BLUE}{path_file}{RESET}')

            if PurePath(path_file).suffix in formats:

                txt_list.append(path_file)
                print(f'Файл текстовый, передаю в режиме STORLINES')
                count_txt += 1

                ftp.storlines('STOR ' + path_file, fobj)
                count_txt_size += ftp.size(path_file)

            else:
                ftp.encoding = 'utf-8'
                ftp.encoding = 'cp1251'
                binary_list.append(path_file)
                print(f'Файл бинарный, передаю в режиме STORBINARY')
                count_binary += 1

                ftp.storbinary('STOR ' + path_file, fobj, 4096)
                count_binary_size += ftp.size(path_file)


            # создаю файл с инфой о переданных текстовых файлах на сервер
            f1 = open('txt_list.txt', 'w', encoding='utf-8')
            f1.write(str('          ' + datetime.today().strftime('%d.%m.%Y')) + '\n' + '\n' + '\n')

            for txt_file in txt_list:
                f1.write(txt_file + '   ---   ')
                f1.write(str(ftp.size(txt_file)) + '   ---   ')
                f1.write(datetime.today().strftime('%d-%m-%Y %H-%M-%S'))
                f1.write('\n' + '\n')

            f1.write(f'Файлы успешно переданны в количестве {count_txt}' + '\n')
            f1.write(f'Размер переданных файлов {count_txt_size}' + ' kb' + '\n')
            f1.write(f'Передача состоялась успешно из {out_dir} в {create_dir}' + '\n')

            # создаю файл с инфой о переданных бинарных файлах на сервер
            f2 = open('binary_list.txt', 'w', encoding='utf-8')
            f2.write(str('          ' + datetime.today().strftime('%d.%m.%Y')) + '\n' + '\n' + '\n')

            for binary_file in binary_list:
                f2.write(binary_file + '   ---   ')
                f2.write(str(ftp.size(binary_file)) + '   ---   ')
                f2.write(time_transfer_txt)
                f2.write('\n' + '\n')

            f2.write(f'Файлы успешно переданы в количестве {count_binary}' + '\n')
            f2.write(f'Размер переданных файлов {count_binary_size}' + ' kb' + '\n')
            f2.write(f'Передача состоялась успешно из {out_dir} в {create_dir}' + '\n')

            # Собираем размер всех переданных файлов
            count_size += ftp.size(path_file)


        # закрываем текстовые файлы
        f1.close()
        f2.close()

        print(
            f'Файл {GREEN}{path_file}{RESET} успешно передан за {YELLOW}{datetime.now() - start_time_file}{RESET} секунд')
        print(f'Размер переданного файла: {ftp.size(path_file)} байт')
        print()
        # добавил длину списка файлов len
    print('Всего файлов переданно:  {}{} из {}{}'.format(GREEN, count, len(onlyfiles), RESET))
    print('Общее время передачи файлов: {}{}{}'.format(YELLOW, datetime.now() - start_time, RESET))
    print(f'Общий размер переданных файлов: {count_size // 1024} килобайт или {count_size} байт')

    # архив переезжает в папку с архивами
    shutil.move(f'{create_dir}.zip', 'archive')
    time.sleep(1)

    # проверяем папку на наличие пустоты
    path_archive = 'archive'
    if not os.listdir(path_archive) == []:
        ftp.mkd(f'archive-{create_dir}')
        ftp.cwd(f'archive-{create_dir}')


        for i in os.listdir(path_archive):
            full_path_archive = Path('archive', i)
            size_archive = os.stat(full_path_archive).st_size

            # передаем файл архива на сервер
            with open(full_path_archive, 'rb') as fobj:

                print(f'Отправляю архив {i} на сервер')
                print(f'Размер передаваемого архива: {size_archive} kb')
                ftp.storbinary('STOR ' + i, fobj)
                print(f'Файл {i} отправлен на сервер')
                time.sleep(1)


            # очищаем папку с архивами
            os.unlink(full_path_archive)

ftp_upload(out_dir)

ftp.quit()
