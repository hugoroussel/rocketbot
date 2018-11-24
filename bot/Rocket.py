import requests
import json
import datetime as dt
import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'").fetchone():
    c.execute('''CREATE TABLE transactions
                 (tx text)''')
    # Save (commit) the changes
    conn.commit()

conn.close()

class Rocket(object):
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
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute("INSERT INTO transactions VALUES (?)", (str(r.json()),))
            conn.commit()
            conn.close()
            print('SOLD {} BTC'.format(amount))
        except:
            pass
        
    @classmethod
    def buy(cls, amount):
        r = requests.post('http://lauzhack.sqpub.ch', data='BUY {} BTC hjgsf348ziogfouzg'.format(amount))
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute("INSERT INTO transactions VALUES (?)", (str(r.json()),))
            conn.commit()
            conn.close()
            print('BROUGHT {} BCT'.format(amount))
        except:
            pass

    @staticmethod
    def team():
        r = requests.get('http://lauzhack.sqpub.ch/teams')
        teams = r.json()
        for team in teams:
            if team['name'] == 'Rocket':
                return team
                
    @classmethod
    def transactions(cls):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        txns = c.execute('SELECT * FROM transactions').fetchall()
        c.close()
        return json.dumps(txns)

    @staticmethod
    def format(transaction):
        [datetime, price] = transaction.split()
        [date, time] = datetime.split('T')
        d = dt.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), hour=int(time[0:2]), minute=int(time[3:5]), second=int(time[6:8]), microsecond=int(time[9:15]))
        return [d, float(price)]
