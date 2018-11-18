# Tests for dht
from model.dht import *
from random import randint

d = DHT(10)

# Add nodes
for i in range(120):
    r = randint(0, 10240)
    d.join(Node(r))

d.update_all_tables()

for i in range(5, 1024, 10):
    d.store(d.start_node, i, "hello" + str(i))

for i in range(5, 200, 10):
    print(d.lookup(d.start_node, i))
