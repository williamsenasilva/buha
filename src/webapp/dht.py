from models import Student
from helper import *

def get_student_from_hd(dht, session, app, academic_id, node_id=None):
    path = make_path_for(dht, session, app, node_id, academic_id)
    return student_from_file(path)

def student_from_file(fullpath):
    try:
        with open(fullpath, 'r') as f:
            s = f.read()
            #print(s)
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

def remove_student_file(dht, session, app, from_node_id, academic_id):
    path = make_path_for(dht, session, app, from_node_id, academic_id)
    student = student_from_file(path)
    if student is not None:
            os.remove(path)

def students_on_node_list(dht, session, app, node_id):
    path = make_path_for(dht, session, app, node_id)
    try:
        lst = sorted(os.listdir(path))
    except FileNotFoundError:
        lst = []
        return []
    lista_academic_id = []
    for name in lst:
        filename, extension = name.split('.')
        lista_academic_id.append(int(filename))
    return lista_academic_id
        

class Node:
    path = None
    def __init__(self, _id, next = None, previous = None):
        self._id = _id
        self.data = dict()
        self.previous = previous
        self.table = [next]

    def store(self, key, value):
        self.data[key] = value
        
    def update_table(self, dht, k):
        del self.table[1:]
        for i in range(1, k):
            self.table.append(dht.find_node(dht.start_node, self._id + 2 ** i))


        
        
class DHT:
    session = None
    app = None
    
    def __init__(self, k, session, app):
        self.session = session
        self.app = app
        self._k = k
        self.size = 2 ** k    
        self.start_node = Node(0, k)
        self.start_node.table[0] = self.start_node
        self.start_node.previous = self.start_node
        self.start_node.update_table(self, k)

    def get_hash_id(self, key):
        return key % self.size

    def distance(self, n1, n2):
        if n1 == n2:
            return 0
        if n1 < n2:
            return n2 - n1
        return self.size - n1 + n2

    def get_number_of_nodes(self):
        if self.start_node == None:
            return 0
        node = self.start_node
        n = 1
        while node.table[0] != self.start_node:
            n = n + 1
            node = node.table[0]
        return n
    
    def find_node(self, start, key):
        hash_id = self.get_hash_id(key)
        current = start
        jumps_number = 0
        while True:
          
            if current._id == hash_id:
                return current
            if self.distance(current._id, hash_id) <= self.distance(current.table[0]._id, hash_id):
                return current.table[0]
            tab_size = len(current.table)
            i = 0
            next_node = current.table[-1]
            while i < tab_size - 1:
                if self.distance(current.table[i]._id, hash_id) < self.distance(current.table[i + 1]._id, hash_id):
                    next_node = current.table[i]
                i = i + 1
            current = next_node
            jumps_number += 1
            
    def lookup(self, start, key):
        node_for_key = self.find_node(start, key)
        if key in node_for_key.data:
            path = make_path_for(self, self.session, self.app, node_for_key._id, key)
            return student_from_file(path)
        return None

    def store(self, start, key, value):
        print("Inserindo no chord o aluno {} com chave {}".format(value.name, key))
        node_for_key = self.find_node(start, key)
        self._store_at(node_for_key, key, value)

    def join(self, new_node):
        print("\33[34m JOIN \33[0m")
        print("\33[34mNovo nó: {}\33[0m".format(new_node._id))
        original_node = self.find_node(self.start_node, new_node._id)

        if original_node._id == new_node._id:
            return
        
        students_on_original_node = students_on_node_list(self, self.session, self.app, original_node._id)

        for key in students_on_original_node:
            print("KEY {}".format(key))
            hash_id = self.get_hash_id(key)
            if self.distance(hash_id, new_node._id) < self.distance(hash_id, original_node._id):
                self._copia_registro(original_node, new_node, key)


        previous_node = original_node.previous
        new_node.table[0] = original_node
        new_node.previous = previous_node
        original_node.previous = new_node
        previous_node.table[0] = new_node
    
        new_node.update_table(self, self._k)

        for key in students_on_original_node:
            hash_id = self.get_hash_id(key)
            if self.distance(hash_id, new_node._id) < self.distance(hash_id, original_node._id):
                self._remove(original_node, key)
                
    def _remove(self, original_node, key):
        print("Removendo registro de {}. ID: {}".format(original_node._id, key))
        remove_student_file(self, self.session, self.app, original_node._id, key)
            
    def _store_at(self, to_node, key, value):
        print("Armazenando {} com chave {} em {}".format(value.name, key, to_node._id))
        path = make_path_for(self, self.session, self.app, to_node._id, key)
        create_file(path, str(value.__dict__).upper())
        to_node.store(key, value)

    def _copia_registro(self, original_node, new_node, key):
        print("Copiando registro de {} para {}. ID: {}".format(original_node._id, new_node._id, key))
        student = get_student_from_hd(self, self.session, self.app, key, original_node._id)
        self._store_at(new_node, key, student)
                      
    def leave(self, node):
        for k, v in node.data.items():
            self._copia_registro(node, node.table[0], k)
        if node.table[0] == node:
            self.start_node = None
        else:
            node.previous.table[0] = node.table[0]
            node.table[0] = previous = node.previous
            if self.start_node == node:
                self.start_node = node.table[0]

    def update_all_tables(self):
        self.start_node.update_table(self, self._k)
        current = self.start_node.table[0]
        while current != self.start_node:
            current.update_table(self, self._k)
            current = current.table[0]