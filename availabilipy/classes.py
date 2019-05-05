import numpy as np
import numpy.linalg as LA
import scipy.optimize as optimize
from typing import List
from collections import OrderedDict

class Node:
    """Describes a Node"""

    def __init__(self, nodeid):
        self.nodeid = nodeid
        self.outgoing = {}
        self.incoming = {}

    def add_path(self, node, weight):
        """ the direction is from self -> node"""

        if node not in self.outgoing:
            self.outgoing[node] = weight
            node.incoming[self] = weight
            return

        raise Exception('That Path already exist')

    def del_path(self, nodeid):

        if nodeid in self.outgoing:
            self.outgoing.pop(nodeid)
            print('Deleted node: '+str(nodeid))
            return

        raise Exception('Path not present in node')

    def __str__(self):

        return f'{self.nodeid}, with {len(self.outgoing)} outgoing edges, and {len(self.incoming)}'

    def __repr__(self):
        return f'Nodeid: {self.nodeid}\nOutgoing: {[node.nodeid for node in self.outgoing]}\nIncoming: {[node.nodeid for node in self.incoming]}'


class MarkovChain:
    """Describes a Markov Chain"""

    def __init__(self, chainid):
        self.nodes: List[Node] = []
        self.chainid = chainid
        self.nodelist = []
        self.availability = None

    def add_node(self, node: Node):
        self.nodes.append(node)

    def del_node(self, node: Node):
        index = self.nodes.index(node)
        self.nodes.pop(index)

    def verify(self):
        """"Makes a deep first search to check if there are nodes that no other node points to"""

        visited = []
        to_visit = [self.nodes[0]]

        while to_visit:
            current_node = to_visit.pop()
            visited.append(current_node)
            to_visit += [node for node in current_node.outgoing if (
                node not in visited) and (node not in to_visit)]

        return {
            'to visit': to_visit,
            'visited': [node.nodeid for node in visited]
        }

    def __convert_to_matrix(self):
        """Obtains the matrix that describes the linear equation system for the CTMC"""

        matrix = np.zeros((len(self.nodes), len(self.nodes)))

        for i, node in enumerate(self.nodes):
            for j, jnode in enumerate(self.nodes):
                if i == j:
                    v = sum([-value for value in node.outgoing.values()])

                else:
                    v = 0 if jnode not in node.incoming else node.incoming[jnode]

                matrix[i, j] = v
        return matrix

    def solve(self):
        """Obtains the probability of being in each state of the CTMC, it returns a dic in the form: {'state id':'probability'}"""
        A = self.__convert_to_matrix()
        B = np.array(np.zeros(len(self.nodes)))
        x = LA.solve(A, B)

        def scalar(x):
            y = np.dot(A, x) - B
            return np.dot(y, y)

        cons = ({'type': 'eq', 'fun': lambda x: x.sum() - 1})
        res = optimize.minimize(scalar, np.zeros(
            len(self.nodes)), method='SLSQP', constraints=cons, options={'disp': False})
        xbest = res['x']
        solution = {}
        for i, node in enumerate(self.nodes):
            solution[node.nodeid] = xbest[i]

        return solution

    def get_availability(self):
        """The nodelist is the list of the nodeids for which the system is considered available"""
        nodelist = self.nodelist
        result = self.solve()
        availability = 0

        for nodeid in nodelist:
            availability = availability + result[nodeid]

        self.availability =availability
        return availability

    def set_nodelist(self, nodelist: list):
        self.nodelist = nodelist

    def __str__(self):
        return f'ID: {self.chainid} \n Nodes: {self.nodes}'

    def to_json(self):

        pos = { node.nodeid:i for i, node in enumerate(self.nodes)}

        return {
            'nodes': [{
                'id': n.nodeid,
            } for n in self.nodes],

            'links': [
                {
                    'source': pos[node.nodeid],
                    'target': pos[link.nodeid],
                    'ratio': value
                } for node in self.nodes for link, value in node.outgoing.items()
            ],
            'selected_states': self.nodelist
        }


class Block:
    "Describes a block from an RBD"

    def __init__(self, blockid: str, isFirst: bool, isLast: bool):
        self.blockid = blockid
        self.outgoing_block = None
        self.incoming_block = None
        self.isFirst = isFirst
        self.isLast = isLast
        self.embedded_chain = None
        self.block_availability = None
        self.amount = 1


    def add_path(self, block):
        """ the direction is from self -> block"""

        if self.outgoing_block is None:
            self.outgoing_block = block
            if block.incoming_block is not None:
                raise Exception(
                    'Block: {} already has an incoming path'.format(block.blockid))
            block.incoming_block = self
            return

        raise Exception('There is already an outgoing path')

    def del_path(self, block):
        if self.outgoing_block == block:
            self.outgoing_block = None
            block.incoming_block = None
            print('Deleted outgoing path')
            return

        elif self.incoming_block == block:
            self.incoming_block = None
            block.outgoing_block = None
            print('Deleted incoming path')
            return

        raise Exception('There is no path pointing to that block')

    def new_chain(self, chainid: str):
        self.embedded_chain = MarkovChain(chainid)

    def embed_chain(self, chain):
        if not type(chain) == MarkovChain:
            raise Exception('You must pass a valid Markov chain object')
        self.embedded_chain = chain
        return

    def delete_embedded_chain(self):
        self.embedded_chain = None
        print('Deleted embedded chain')
        return

    def calc_availability(self):
        if self.embedded_chain == None:
            raise Exception('There is no embedded chain')

        if self.embedded_chain.nodelist == None or len(self.embedded_chain.nodelist) == 0:
            raise Exception(
                'You need to define a list with all available nodes and that list can not be empty')

        for nodeid in self.embedded_chain.nodelist:
            if self.embedded_chain.nodelist.count(nodeid) > 1:
                raise Exception('You have repeated nodes')

        self.block_availability = self.embedded_chain.get_availability(

        )
        return self.block_availability

    def __str__(self):
        return f'ID: {self.blockid} \n Outgoing: {self.outgoing_block.blockid if self.outgoing_block is not None else self.outgoing_block} \n Incoming: {self.incoming_block.blockid if self.incoming_block is not None else self.incoming_block} \n Is First: {str(self.isFirst)} \n Is Last: {str(self.isLast)} \n Chain {str(self.embedded_chain)} \n Availability {str(self.block_availability)}'


class Parallel_Block:
    "Describes a paralel block from an RBD"

    def __init__(self, blockid: str, isFirst: bool, isLast: bool, amount: int, valid: int):
        """Amount is the amount of parallel blocks and valid is the quantity of blocks 
        that need to be active for the system to work"""
        if amount < 2 or amount > 4 or valid == 0 or valid > amount:
            raise Exception('Invalid amount of blocks and/or valid blocks')
        self.blockid = blockid
        self.outgoing_block = None
        self.incoming_block = None
        self.isFirst = isFirst
        self.isLast = isLast
        self.embedded_chain = None
        self.block_availability = None
        self.amount = amount
        self.valid = valid

    def add_path(self, block):
        """ the direction is from self -> block"""
        if self.outgoing_block is None:
            self.outgoing_block = block
            if block.incoming_block is not None:
                raise Exception(
                    'Block: {} already has an incoming path'.format(block.blockid))
            block.incoming_block = self
            return

        raise Exception('There is already an outgoing path')

    def del_path(self, block):
        if self.outgoing_block == block:
            self.outgoing_block = None
            block.incoming_block = None
            print('Deleted outgoing path')
            return

        elif self.incoming_block == block:
            self.incoming_block = None
            block.outgoing_block = None
            print('Deleted incoming path')
            return

        raise Exception('There is no path pointing to that block')

    def new_chain(self, chainid: str):
        self.embedded_chain = MarkovChain(chainid)
        return

    def embed_chain(self, chain):
        if not type(chain) == MarkovChain:
            raise Exception('You must pass a valid Markov chain object')
        self.embedded_chain = chain
        return

    def delete_embedded_chain(self):
        self.embedded_chain = None
        print('Deleted embedded chain')
        return

    def calc_availability(self):
        if self.embedded_chain == None:
            raise Exception('There is no embedded chain')

        if self.embedded_chain.nodelist == None or len(self.embedded_chain.nodelist) == 0:
            raise Exception(
                'You need to define a list with all available nodes')

        for nodeid in self.embedded_chain.nodelist:
            if self.embedded_chain.nodelist.count(nodeid) > 1:
                raise Exception('You have repeated nodes')

        avail = self.embedded_chain.get_availability()

        if self.amount == 2:
            if self.valid == 1:
                self.block_availability = 1 - (1-avail)**2
            else:
                self.block_availability = avail**2

        elif self.amount == 3:
            if self.valid == 1:
                self.block_availability = 1 - (1-avail)**3

            elif self.valid == 2:
                self.block_availability = avail**3 + 3*avail**2 - (1-avail)

            else:
                self.block_availability = avail**3

        else:
            if self.valid == 1:
                self.block_availability = 1 - (1-avail)**4

            elif self.valid == 2:
                self.block_availability = avail**4 + 4 * \
                    avail**3*(1-avail) + 6*avail**2*(1-avail)**2

            elif self.valid == 3:
                self.block_availability = avail**4 + 4*avail**3*(1-avail)

            else:
                self.block_availability = avail**4
        return self.block_availability

    def __str__(self):
        return f'ID: {self.blockid} \n Outgoing: {self.outgoing_block.blockid if self.outgoing_block is not None else self.outgoing_block} \n Incoming:\
        {self.incoming_block.blockid if self.incoming_block is not None else self.incoming_block} \n Is First: {str(self.isFirst)} \n Is Last: {str(self.isLast)} \n Chain:\
        {str(self.embedded_chain)} \n Availability {str(self.block_availability)}'


class RBD:
    """Describes a RBD"""

    def __init__(self, rbdid: str):
        self.blocks = []
        self.availability = None
        self.rbdid = rbdid

    def add_block(self, block: Block):
        for block_element in self.blocks:
            
            if block_element.blockid == block.blockid:
                raise Exception('Block already in chain')
        self.blocks.append(block)
        return

    def delete_block(self, blockid):
        for block_element in self.blocks:
            
            if block_element.blockid == blockid:
                self.blocks.pop(self.blocks.index(block_element))
                return
            else:
                pass

        raise Exception('That block is not in this RBD')

    def solve_rbd(self):
        availability = 1
        for block in self.blocks:
            print('id: '+block.blockid)
            calculated = block.calc_availability()
            print('block availability: ' + str(calculated))
            availability = availability*calculated
            print('current availability: ' + str(availability))

        self.availability = availability
        return self.availability

    def to_json(self):
    
        pos = { block.blockid:i for i, block in enumerate(self.blocks)}
        return {
            'blocks': [{
                'id': n.blockid,
                'amount': n.amount,
                'availability': round(n.embedded_chain.availability,4) if n.embedded_chain.availability else None,
                'chainid': n.embedded_chain.chainid if n.embedded_chain else None,
                'valid': n.valid if type(n)==Parallel_Block else 0
            } for n in self.blocks],

            'links': [
                {
                    'source': pos[block.blockid],
                    'target': pos[block.outgoing_block.blockid],
                } for block in self.blocks if block.outgoing_block 
            ],
        }

    def __str__(self):
        return f'Availability: {self.availability} \n Blocks: {self.blocks}'
