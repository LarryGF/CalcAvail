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
    x = MarkovChain(chainid)
    persistent_data['chains'][chainid] = x
    current_chain = x
    return chainid


@eel.expose
def hello():
    print('fatso')
    return 'hello fat'


@eel.expose
def get_initial_data(route):
    current_chain = persistent_data['chains'][route.split('/markov/')[1]]
    x = current_chain.to_json()
    print(type(current_chain))

    return x 


@eel.expose
def get_data():
    return current_chain.to_json()

@eel.expose
def add_node(name):
    current_chain.add_node(Node(name))
    return True


if __name__ == "__main__":
    eel.start('index.html', options={'port': 8686})
