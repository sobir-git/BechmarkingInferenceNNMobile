import os

def abs_listdir(path):
    '''Lists absolute paths of files in a directory.'''

    # convert to absolute path
    path = os.path.abspath(path)
    return [os.path.join(path, f) for f in os.listdir(path)]
