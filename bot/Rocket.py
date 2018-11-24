import requests

class Rocket(object):
    @staticmethod
    def get(callback):
        r = requests.get('http://lauzhack.sqpub.ch/prices', stream=True)
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                callback(decoded_line)

    @staticmethod
    def sell(amount):
        r = requests.post('http://lauzhack.sqpub.ch', data='SELL {} BTC hjgsf348ziogfouzg'.format(amount))
        print('SOLD {} BTC'.format(amount))
        
    @staticmethod
    def buy(amount):
        r = requests.post('http://lauzhack.sqpub.ch', data='BUY {} BTC hjgsf348ziogfouzg'.format(amount))
        print('BROUGHT {} BCT'.format(amount))
