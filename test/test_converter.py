from availabilipy.classes import *

def test_to_front():
    x = MarkovChain('tu madre')

    assert x.to_json() == {'nodes':[], 'links':[]}

    n1 = Node('n1')
    n2 = Node('n2')
    n3 = Node('n3')
    n4 = Node('n4')
    x.add_node(n1)
    x.add_node(n2)
    x.add_node(n3)
    x.add_node(n4)


    assert x.to_json() == {
        'nodes': [
            {'id': 'n1'},
            {'id': 'n2'},
            {'id': 'n3'},
            {'id': 'n4'},
        ],
        'links': []
    }

    n1.add_path(n2,2.5)
    n1.add_path(n3,123)
    n2.add_path(n1,3.4)
    n2.add_path(n3,49.87)
    n3.add_path(n1,1.999923)
    n3.add_path(n2,4.78)
    n4.add_path(n1, 1.99)
    
    assert x.to_json() == {
        'nodes': [
            {'id': 'n1'},
            {'id': 'n2'},
            {'id': 'n3'},
            {'id': 'n4'},
        ],
        'links': [
            {
                'source': 0,
                'target': 1,
                'text': '2.5'
            },
            {
                'source': 0,
                'target': 2,
                'text': '123'
            },
            {
                'source': 1,
                'target': 0,
                'text': '3.4'
            },
            {
                'source': 1,
                'target': 2,
                'text': '49.87'
            },
            {
                'source': 2,
                'target': 0,
                'text': '1.999923'
            },
            {
                'source': 2,
                'target': 1,
                'text': '4.78'
            },
            {
                'source': 3,
                'target': 0,
                'text': '1.99'
            }
        ]
    }