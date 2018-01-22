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

def LoadPath(): # Load the path from the config file, If not found return None, None
    SAMP_PATH, LOG_PATH = None, None

    if not os.path.exists('config.cfg'):
        Log('Unable to find config file.')
        exit(0)
    
    with open('config.cfg', 'r') as f:
        l = 1
        for line in f.readlines():
            if len(line.strip('\n').replace(' ', '')) != 0 and os.path.exists(line.strip('\n')):
                if l == 1:
                    l = 2
                    SAMP_PATH = line.strip('\n')
                elif l == 2:
                    LOG_PATH = line.strip('\n')
                    break
    if SAMP_PATH[-1] == "\\":
        SAMP_PATH = SAMP_PATH[:-1]
        
    if LOG_PATH[-1] == "\\":
        LOG_PATH = LOG_PATH[:-1]
        
    return SAMP_PATH, LOG_PATH

Log('\n\n')

SAMP_PATH, LOG_PATH = LoadPath()
WMI = GetObject('winmgmts:')

if SAMP_PATH is None: # If path added.
    Log('Unable to find a VALID SAMP Path, Default path would be used.')
    SAMP_PATH = "%s/%s/Documents/GTA San Andreas User Files/SAMP/" % (os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'))

if not os.path.exists(SAMP_PATH+'\\sa-mp.cfg'):
    Log('Unable to find a VALID SAMP Path, Exiting...')
    exit(0)

if LOG_PATH is None:
    Log('Unable to find a valid path to save the logs, Using Default path in SAMP Doc. Folder.')
    LOG_PATH = "%s\\SavedLogs" % (SAMP_PATH)
    system("mkdir \"%s\\SavedLogs\"" % (SAMP_PATH))
    Log('SavedLogs Folder created.')

def IsGtaRunning(): # The name is clear enough.
    processes = WMI.InstancesOf('Win32_Process')
    processes = [process.Properties_('Name').Value for process in processes]
    if "gta_sa.exe" in processes:
        return True
    else:
        return False

def SaveLog():
    with open(SAMP_PATH+'\\chatlog.txt', 'r') as f:
        d = f.read()
    
    # Year Month Day Hour Mn Second
    fname = 'Log_File_%d_%d_%d_%d_%d_%d.txt' % (datetime.now().year, datetime.now().month, datetime.now().day,
                                            datetime.now().hour, datetime.now().minute, datetime.now().second)
    
    with open(LOG_PATH+'\\'+fname, 'w') as f:
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


