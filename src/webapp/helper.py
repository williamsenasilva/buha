import os
import ast
from models import Student
from dht import DHT, Node



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

def student_from_file(fullpath):
    try:
        with open(fullpath, 'r') as f:
            s = f.read()
            print(s)
            data = ast.literal_eval(s)
    except FileNotFoundError:
        return None

    name = data['NAME']
    university = data['UNIVERSITY']
    academic_id = data['ACADEMIC_ID']
    buha_id = data['BUHA_ID']
    student = Student({
                        "name": name, 
                        "university": university, 
                        "academicID": academic_id, 
                        "buha_id":buha_id
                        })  
    return student

def make_path_for(dht, session, app, node_id=None, academic_id=None):
    base_path = app.root_path + "/static/dht/"
    base_path += session.get('moment') +'/' 
    if (node_id is None) and (academic_id is None):
        return base_path
    if node_id is None:
        node_ref = dht.find_node(dht.start_node, academic_id)._id
    else:
        node_ref = node_id
    if academic_id is None:
        return base_path + str(node_ref) + '/'
    else:
        return base_path + str(node_ref) + '/' + str(academic_id)+'.txt'      

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