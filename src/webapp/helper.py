import os

def read_file(fullpath):
    file = open(fullpath, 'r')
    text = file.readlines()
    print(text)
    arquivo.close()

def create_file(fullpath,text):
    file = open(fullpath, 'w')
    file.writelines(text)
    file.close()

def update_file(fullpath,newline):
    file = open(fullpath, 'r')
    text = file.readlines()
    file.close()
    text.append(newline + "\n") 
    file = open(fullpath, 'w')
    file.writelines(text)
    file.close()

def make_tree(path):
    tree = dict(name=path, children=[])
    try: 
        lst = sorted(os.listdir(path))
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=fn))
    return tree