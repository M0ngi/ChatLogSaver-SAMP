"""

    This script would save your chatlogs right after leaving the game.
    Log files would be found in 'Documents/GTA San Andreas User Files/SavedLogs/'

"""

__author__      = "M. Mongi Saidane"
__version__     = "1.0"
__email__       = "saidanemongi@gmail.com"

from win32com.client import GetObject
import os.path, time
from os import system
from datetime import datetime

def Log(txt):
    try:
        open('LogFile.txt', 'r')
    except IOError:
        open('LogFile.txt', 'w')

    txt = '%d/%d/%d %d-%d-%d: %s' % (datetime.now().year, datetime.now().month, datetime.now().day,
                                     datetime.now().hour, datetime.now().minute, datetime.now().second,
                                     txt)

    with open('LogFile.txt', 'a') as f:
        f.write(txt+'\n')
    return True

WMI = GetObject('winmgmts:')
SAMP_PATH = "%s/%s/Documents/GTA San Andreas User Files/SAMP/" % (os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'))

if not os.path.exists(SAMP_PATH+'sa-mp.cfg'):
    Log('Unable to find SAMP Path, Exiting...')
    exit(0)

if not os.path.exists(SAMP_PATH+'SavedLogs/'):
    system("mkdir \"%sSavedLogs\"" % (SAMP_PATH))
    Log('SavedLogs Folder created.')

def IsGtaRunning():
    processes = WMI.InstancesOf('Win32_Process')
    processes = [process.Properties_('Name').Value for process in processes]
    if "gta_sa.exe" in processes:
        return True
    else:
        return False

def SaveLog():
    with open(SAMP_PATH+'chatlog.txt', 'r') as f:
        d = f.read()
    
    # Year Month Day Hour Mn Second
    fname = 'Log_File_%d_%d_%d_%d_%d_%d.txt' % (datetime.now().year, datetime.now().month, datetime.now().day,
                                            datetime.now().hour, datetime.now().minute, datetime.now().second)
    
    with open(SAMP_PATH+'SavedLogs/'+fname, 'w') as f:
        f.write(d)
    return 1

def Main():
    # Wait till the game start
    while True:
        if IsGtaRunning():
            break
        else:
            time.sleep(1)
    
    # Now wait till the game stops (T/O, Quit)
    while True:
        if not IsGtaRunning():
            break
        else:
            time.sleep(1)

    # Save Chat
    SaveLog()

    # Update log file
    Log('Chat log saved.')
    return 1

if __name__ == '__main__':
    # Continue Running & Checking
    while True:
        Main()


