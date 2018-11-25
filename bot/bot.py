import pickle
import neat
from Rocket import *

if __name__ == '__main__':
    winner = pickle.load(open('winner.pkl', 'rb'))
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-v1')

    ff = neat.nn.feed_forward.FeedForwardNetwork.create(winner, config)
    
    refPrice = 0
    
    ma5 = []
    ma10 = []
    ma20 = []
    
    def callback(input):
        global refPrice
        global ma5
        global ma10
        global ma20
        team = Rocket.team()
        [time, price] = input
        if refPrice == 0:
            refPrice = price
        ma5.append(input)
        ma5 = list(filter(lambda x: (time - x[0]).total_seconds() < 300, ma5))
        ma10.append(input)
        ma10 = list(filter(lambda x: (time - x[0]).total_seconds() < 600, ma10))
        ma20.append(input)
        ma20 = list(filter(lambda x: (time - x[0]).total_seconds() < 1200, ma20))
        print(sum(map(lambda x: x[1], ma20)) / len(ma20))
        print(refPrice)
        [bs, ex, qu] = ff.activate((
            price / refPrice,
            sum(map(lambda x: x[1], ma5)) / len(ma5) / refPrice,
            sum(map(lambda x: x[1], ma10)) / len(ma10) / refPrice,
            sum(map(lambda x: x[1], ma20)) / len(ma20) / refPrice,
            team['cash'] / 100000,
            team['XBT'] / (100000/refPrice)
        ))
        
        print(bs)
        print(ex)
        print(qu)
        if ex > 0 and qu > 0.0001:
            if bs > 0:
                Rocket.buy(0.99*((qu + 1) / 2) * team['cash'] / price)
            else:
                Rocket.sell(0.99*((qu + 1) / 2) * team['XBT'])
    
    Rocket.get(callback)
