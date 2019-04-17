import eel
from availabilipy.classes import *

x = MarkovChain('tu madre')


n1 = Node('n1')
n2 = Node('n2')
n3 = Node('n3')
n4 = Node('n4')
x.add_node(n1)
x.add_node(n2)
x.add_node(n3)
x.add_node(n4)



n1.add_path(n2, 2.5)
n1.add_path(n3, 1.3)
n2.add_path(n1, 3.4)
n2.add_path(n3, 1.87)
n3.add_path(n1, 1.999)
n3.add_path(n2, 4.78)
n4.add_path(n1, 1.99)


eel.init('dist')


@eel.expose
def hello():
    print('fatso')
    return 'hello fat'

@eel.expose
def data():
    return x.to_json()

eel.start('index.html', options={'port': 8686})
