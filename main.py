import eel
import random
import json
import os
import fs
from availabilipy.classes import *

os.makedirs('saves', exist_ok=True)
save_folder = os.path.join(os.getcwd(),'saves')
persistent_data = {
    'chains': {},
    'rbd': {}

}


eel.init('dist')

#################################### General ########################################################################
@eel.expose
def save(name):
    print("Saving to json")
    if os.path.exists(name + '.json'):
        return 'That file already exists'
    try:
        file = open(os.path.join(save_folder,name+'.json'), 'w')
        data = {
            'rbd': persistent_data['rbd'].to_json(),
            'chains': {persistent_data['chains'][chain].chainid: persistent_data['chains'][chain].to_json() for chain in persistent_data['chains']}
        }
        json.dump(data, file)
        file.close()
        return True
        
    except Exception as e:
        return str(e)

@eel.expose
def prepare_load():
    saves_dir = fs.open_fs(save_folder)
    saves_list = list(saves_dir.filterdir(path='.', files=['*.json'], exclude_dirs=['*']))
    saves_list = [save.name for save in saves_list]
    return saves_list

@eel.expose
def load(name):
    print("Loading from json")
    try:
        file = open(os.path.join(save_folder,name))
        data = json.load(file)
        print(data)
        file.close()
        create_rbd()
        load_blocks(data['rbd']['blocks'])
        load_links(data['rbd']['links'])
        load_chains(data['chains'], data['rbd']['blocks'])
        return True

    except Exception as e:
        print(str(e))
        return str(e)


def load_blocks(blocks):
    print("Loading blocks")

    for block in blocks:
        add_block(block['amount'], block['id'], block['valid'])
        test_block = search_block(block['id'])
        
        test_block.block_availability =  block['availability']
        print(test_block)

def load_links(links):
    print("Loading links")

    for link in links:
        add_path(persistent_data['rbd'].blocks[link['source']].blockid,
                 persistent_data['rbd'].blocks[link['target']].blockid)


def load_chains(chains, blocks):
    print("Loading chains")
    global current_chain
    for block in blocks:
        chainid = block['chainid']
        if chainid:
            current_block = search_block(block['id'])
            current_chain = MarkovChain(chainid)
            persistent_data['chains'][chainid] = current_chain
            current_block.embed_chain(current_chain)
            current_chain.availability = current_block.block_availability
            chain_specs = chains[chainid]
            for node in chain_specs['nodes']:
                add_node(node['id'])

            for link in chain_specs['links']:
                from_node = current_chain.nodes[link['source']]
                to_node = current_chain.nodes[link['target']]
                add_transition(from_node.nodeid, to_node.nodeid, link['ratio'])

        else:
            pass

######################################## RBD ########################################################################


@eel.expose
def create_rbd():
    print('Creating rbd')
    try:
        if persistent_data['rbd']:
            return True

        rbd = RBD('rbd')

        persistent_data['rbd'] = rbd

        return True

    except Exception as e:
        return str(e)


@eel.expose
def get_rbd():
    print('Getting RBD')
    try:
        print(persistent_data)

        print('to json')
        print(persistent_data['rbd'].to_json())
       
        # if len(persistent_data['rbd'].to_json())==0:
        #     block = Block('B0')
        #     persistent_data['rbd'].add_block(block)

        return persistent_data['rbd'].to_json()

    except Exception as e:
        print(str(e))
        return str(e)


@eel.expose
def add_block(number, id, active):
    print('Adding Block')
    try:
        if int(number) > 1:
            block = Parallel_Block(id, False, False, number, active)
        else:
            block = Block(id, False, False)
        persistent_data['rbd'].add_block(block)
        return True

    except Exception as e:
        return str(e)


@eel.expose
def add_path(fromBlock, toBlock):
    print('Adding path')
    try:
        fromB = search_block(fromBlock)
        toB = search_block(toBlock)

        if toB.outgoing_block == fromB:
            return 'The destination block has an outgoing path to the source block'
        else:
            fromB.add_path(toB)
        return True

    except Exception as e:
        return str(e)


@eel.expose
def del_path(data):
    print('Deleting path')
    try:
        blocks = data.split('=>')
        block = search_block(blocks[0])
        to_delete = search_block(blocks[1])
        block.del_path(to_delete)
        return True
    except Exception as e:
        return str(e)


@eel.expose
def del_block(data):
    print('Deleting block')
    try:
        block = search_block(data)
        if block.outgoing_block:
            block.del_path(block.outgoing_block)
        for current_block in persistent_data['rbd'].blocks:
            if current_block.outgoing_block == block:
                current_block.del_path(current_block.outgoing_block)

        persistent_data['rbd'].delete_block(data)
        return True

    except Exception as e:
        return str(e)


@eel.expose
def attach_chain(data):
    global current_chain
    print('Attaching Chain')
    try:
        block = search_block(data)
        if block.embedded_chain:
            return block.embedded_chain.chainid

        chainid = str(random.randint(1, 10000))
        while chainid in persistent_data['chains'].keys():
            chainid = str(random.randint(1, 10000))
        current_chain = MarkovChain(chainid)
        persistent_data['chains'][chainid] = current_chain
        block.embed_chain(current_chain)

        return chainid

    except Exception as e:
        return str(e)


@eel.expose
def solve_rbd():
    print('Solving RBD')
    try:
        persistent_data['rbd'].solve_rbd()
        return (round(persistent_data['rbd'].availability, 5), True)

    except Exception as e:
        return (str(e), False)

@eel.expose
def set_availability(block, amount):
    try:
        block = search_block(block)
        block.block_availability = float(amount)
        if block.embedded_chain:
            block.embedded_chain.availability = float(amount)

        return True
    except Exception as e:
        return str(e)

############################################# CTMC #################################################################


@eel.expose
def get_initial_data(route):
    print('Getting chain for the first time')
    global current_chain
    try:
        current_chain = persistent_data['chains'][route.split('/markov/')[1]]
        print(current_chain.chainid)
        print(current_chain.to_json())
        return current_chain.to_json()

    except Exception as e:
        return str(e)


@eel.expose
def get_data():
    print('Getting Chain')
    try:
        print(current_chain.chainid)
        print(current_chain.to_json())
        return current_chain.to_json()

    except Exception as e:
        return str(e)

@eel.expose
def add_node(name):
    print('Adding node')
    try:
        current_chain.add_node(Node(name))
        return True

    except Exception as e:
        return str(e)

@eel.expose
def add_transition(from_node, to_node, ratio):
    print('Adding transition')
    try:
        from_node = search_node(from_node)
        if not from_node:
            return False
        to_node = search_node(to_node)
        if not to_node:
            return False
        from_node.add_path(to_node, float(ratio))
        return True

    except Exception as e:
        return str(e)

@eel.expose
def delete_transition(data):
    print('Deleting transition')
    try:
        nodes = data.split('=>')
        print(nodes)
        node = search_node(nodes[0])
        to_delete = search_node(nodes[1])
        node.del_path(to_delete)
        return True

    except Exception as e:
        return str(e)

@eel.expose
def delete_node(data):
    print('Deleting node')
    try:
        node = search_node(data)
        if node:
            current_chain.del_node(node)
            return True
        else:
            return "You haven't selected a node"

    except Exception as e:
        return str(e)

@eel.expose
def set_nodelist(nodelist):
    print('Setting available nodes')
    try:
        current_chain.set_nodelist(nodelist)
        print(current_chain.nodelist)
        return True

    except Exception as e:
        return str(e)

@eel.expose
def solve_chain():
    print('Solving chain')
    try:
        result = current_chain.get_availability()

        return (round(result, 5),True)

    except Exception as e:
        return (str(e),False)


def search_node(nodeid):
    print(current_chain.chainid)
    for node in current_chain.nodes:
        if node.nodeid == nodeid:
            return node

    return False


def search_block(blockid):
    for block in persistent_data['rbd'].blocks:
        if block.blockid == blockid:
            return block

    return False


if __name__ == "__main__":
    eel.start('index.html', options={'port': 8686})
