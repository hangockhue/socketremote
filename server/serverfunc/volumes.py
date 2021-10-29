import os.path

dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_volumes():
    return { 'volumes': ['%s:' % d for d in dl if os.path.exists('%s:' % d)] }
