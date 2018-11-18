class Node:
    
    def __init__(self, _id, next = None, previous = None):
        self._id = _id
        self.data = dict()
        self.previous = previous
        self.table = [next]

    def update_table(self, dht, k):
        del self.table[1:]
        for i in range(1, k):
            self.table.append(dht.find_node(dht.start_node, self._id + 2 ** i))
        
class DHT:
    
    def __init__(self, k):
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
            i = 0;
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
            return node_for_key.data[key]
        return None

    def store(self, start, key, value):
        node_for_key = self.find_node(start, key)
        node_for_key.data[key] = value

    def join(self, new_node):
        original_node = self.find_node(self.start_node, new_node._id)

        if original_node._id == new_node._id:
            return
        
        for key in original_node.data:
            hash_id = self.get_hash_id(key)
            if self.distance(hash_id, new_node._id) < self.distance(hash_id, original_node._id):
                new_node.data[key] = original_node.data[key]

        previous_node = original_node.previous
        new_node.table[0] = original_node
        new_node.previous = previous_node
        original_node.previous = new_node
        previous_node.table[0] = new_node
    
        new_node.update_table(self, self._k)

        for key in list(original_node.data.keys()):
            hash_id = self.get_hash_id(key)
            if self.distance(hash_id, new_node._id) < self.distance(hash_id, original_node._id):
                del original_node.data[key]
                
    def leave(self, node):
        for k, v in node.data.items():
            node.table[0].data[k] = v
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