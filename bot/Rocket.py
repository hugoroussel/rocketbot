import requests
import datetime as dt

class Rocket(object):
    txns = []
    
    @staticmethod
    def get(callback):
        r = requests.get('http://lauzhack.sqpub.ch/prices', stream=True)
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                callback(Rocket.format(decoded_line))

    @classmethod
    def sell(cls, amount):
        r = requests.post('http://lauzhack.sqpub.ch', data='SELL {} BTC hjgsf348ziogfouzg'.format(amount))
        cls.txns.append(r.json())
        print('SOLD {} BTC'.format(amount))
        
    @classmethod
    def buy(cls, amount):
        r = requests.post('http://lauzhack.sqpub.ch', data='BUY {} BTC hjgsf348ziogfouzg'.format(amount))
        cls.txns.append(r.json())
        print('BROUGHT {} BCT'.format(amount))

    @staticmethod
    def team():
        r = requests.get('http://lauzhack.sqpub.ch/teams')
        teams = r.json()
        for team in teams:
            if team['name'] == 'Rocket':
                return team
                
    @classmethod
    def transactions(cls):
        return cls.txns

    @staticmethod
    def format(transaction):
        [datetime, price] = transaction.split()
        [date, time] = datetime.split('T')
        d = dt.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), hour=int(time[0:2]), minute=int(time[3:5]), second=int(time[6:8]), microsecond=int(time[9:15]))
        return [d, float(price)]
