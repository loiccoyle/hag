from shutil import which

def check_cmd(cmd):
    '''Check is cmd is installed.
    '''
    return which(cmd) is not None
