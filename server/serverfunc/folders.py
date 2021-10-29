from os import path, listdir

def list_folders(dir):
    result = { 'files': [], 'folders': [] }

    if path.exists(dir):
        if path.isdir(dir):
            items = listdir(dir)

            for item in items:
                if path.isfile(path.join(dir, item)):
                    result['files'].append(item)
                else:
                    result['folders'].append(item) 

    return result