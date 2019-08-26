import os

def rm_if_exits(path):
    if os.path.exists(path):
        os.remove(path)
