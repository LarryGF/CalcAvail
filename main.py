import eel

eel.init('dist')

@eel.expose
def hello():
    print('fatso')
    return 'hello fat'


eel.start('index.html' ,options={'port': 8686})


