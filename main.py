import eel
import random
from availabilipy.classes import *

persistent_data = {
    'chains': {},
    'rbd': {}

}



eel.init('dist')


@eel.expose
def create_chain():
    global current_chain
    chainid = str(random.randint(1, 10000))
    while chainid in persistent_data['chains'].keys():
        chainid = str(random.randint(1, 2))
    current_chain = MarkovChain(chainid)
    persistent_data['chains'][chainid] = current_chain
    
    return chainid


@eel.expose
def hello():
    print('fatso')
    return 'hello fat'


@eel.expose
def get_initial_data(route):
    global current_chain
    current_chain = persistent_data['chains'][route.split('/markov/')[1]]
    print(current_chain.chainid)
    print(current_chain.to_json())
    return current_chain.to_json()


@eel.expose
def get_data():
    print(current_chain.chainid)
    print(current_chain.to_json())
    return current_chain.to_json()

@eel.expose
def add_node(name):
    current_chain.add_node(Node(name))
    return True

@eel.expose
def add_transition(from_node, to_node, ratio):
    from_node = get_node(from_node)
    if not from_node:
        return False
    to_node = get_node(to_node)
    if not to_node:
        return False
    from_node.add_path(to_node,float(ratio))
    return True

@eel.expose
def delete_transition(data):
    nodes = data.split('=>')
    print(nodes)
    node = get_node(nodes[0])
    to_delete = get_node(nodes[1])
    node.del_path(to_delete)
    return True

@eel.expose
def delete_node(data):
    node = get_node(data)
    if node:
        current_chain.del_node(node)
        return True
    else:
        return False

@eel.expose
def set_nodelist(nodelist):
    current_chain.set_nodelist(nodelist)
    print(current_chain.nodelist)
    return True

@eel.expose
def solve_chain():
    result = current_chain.get_availability()
    return result

def get_node(nodeid):
    print(current_chain.chainid)
    for node in current_chain.nodes:
        if node.nodeid == nodeid:
            return node
    
    return False


if __name__ == "__main__":
    eel.start('index.html', options={'port': 8686})
