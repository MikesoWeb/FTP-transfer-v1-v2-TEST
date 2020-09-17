import ftplib

import colorama

# ftp = ftplib.FTP('185.114.245.109', timeout=10)
# ftp.login(user='cq51725_admin', passwd='MpV6dwCa')

"""Beget"""


#
# ftp = ftplib.FTP('klionp9p.beget.tech', timeout=10)
# ftp.login(user='klionp9p_lesson', passwd='2zFh%Ek3')
#
GREEN = colorama.Fore.GREEN
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.LIGHTYELLOW_EX
BLUE = colorama.Fore.LIGHTBLUE_EX
#
# print(ftp.connect())
# ftp.connect()
# ftp.dir()
formats = ['.txt', '.html', '.docx', '.htm']

from ftplib import FTP_TLS
ftp=FTP_TLS()
# ftp.set_debuglevel(2)
ftp.connect('klionp9p.beget.tech', 21, timeout=100)
ftp.sendcmd('USER klionp9p_lesson')
ftp.sendcmd('PASS 3M1l&Mha')
ftp.cwd('klionp9p.beget.tech')
# ftp.dir()
# ftp.retrlines('LIST')


