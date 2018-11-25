from Rocket import *
import random

if __name__ == '__main__':
    
    def callback(input):
        [time, price] = input
        team = Rocket.team()
        y = random.randint(0, 9)
        x = random.normalvariate(0, 0.1)
        if x < 0 and x > -1 and y == 0:
            Rocket.buy(0.99 * (- x) * team['cash'] / price)
        elif x > 0 and x < 1 and y == 0:
            Rocket.sell(0.99 * x * team['XBT'])
    
    Rocket.get(callback)
