from ftp_config import *
from datetime import datetime
ftp.cwd('testovaya')
ftp.encoding = 'utf-8'


formats = ['txt', 'mp4']


def ftp_upload(path):
    """
    Функция для загрузки файлов на FTP-сервер
    @param ftp_obj: Объект протокола передачи файлов
    @param path: Путь к файлу для загрузки
    """


    start_time = datetime.now()
    print(f'...началась передача файла {path}')
    with open(path, 'rb') as fobj:


        if path.split('.')[1] in formats:
            ftp.encoding = 'cp1251'

        if path.split('.')[1] == 'mp3':
            ftp.encoding = 'utf-8'

            # ftp.encoding = 'cp1251'
        ftp.storbinary('STOR ' + path, fobj)
    print(f'Файл {path} успешно передан за {datetime.now() - start_time} секунд')



def test():
    count=0
    start_time = datetime.now()


    # Отправляет файлы на сервер в корневую папку
    path = 'test/1.txt'
    ftp_upload(path)
    count += 1

    path_rus = 'test/Русский текстовый файл.txt'
    ftp_upload(path_rus)
    count += 1

    # Отправляет файлы на сервер в корневую папку
    jpg_path = 'test/1_copy.jpg'
    ftp_upload(jpg_path)
    count += 1

    path = 'ticketSonja.png'
    ftp_upload(path)
    count += 1

    path_music = 'Dense - Echoes from San Ibé.mp3'
    ftp_upload(path_music)
    count += 1

    path_music_two = 'test/БРАВО - Ветер знает.mp3'
    ftp_upload(path_music_two)
    count += 1

    # Проблема с кодировкой,  русские имена записываются как Р­С‚Рѕ РјРѕРё РіСЂРёР±С‹.mp4
    path_video = 'test/Это мои грибы.mp4'
    ftp_upload(path_video)
    count += 1

    path_video = 'It`s my mushrooms.mp4'
    ftp_upload(path_video)
    count += 1

    print('Всего переданно {}'.format(count))
    print('Общее время передачи файлов: {}'.format(datetime.now() - start_time))

test()
ftp.quit()
