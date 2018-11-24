import pickle
import neat
from Rocket import *

if __name__ == '__main__':
    winner = pickle.load(open('winner.pkl', 'rb'))
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-v1')

    ff = neat.nn.feed_forward.FeedForwardNetwork.create(winner, config)
    
    def callback(input):
        team = Rocket.team()
        [time, price] = input
        print(ff.activate((price, team['cash'], team['XBT'])))
        print(price)
    
    Rocket.get(callback)
