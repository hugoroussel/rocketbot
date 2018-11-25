from Rocket import *
import random

if __name__ == '__main__':
    
    def callback(input):
        [time, price] = input
        teams = Rocket.teams()
        if not teams:
            return
        best = 0
        bestTeam = None
        rocketTeam = None
        for team in teams:
            if best < (team['cash'] + team['assets']) and team['cash'] != 100000:
                bestTeam = team
                best = team['cash'] + team['assets']
            if team['name'] == 'Rocket':
                rocketTeam = team
                
        if not bestTeam:
            return
        
        if bestTeam['name'] == 'Rocket':
            if rocketTeam['assets'] + rocketTeam['cash'] > 100350:
                return
            
        if bestTeam['assets'] == 0:
            if rocketTeam['assets'] != 0:
                Rocket.sell(rocketTeam['XBT'])
        else:
            bestCashRatio = bestTeam['cash'] / (bestTeam['assets'] + bestTeam['cash'])
            rocketCashRatio = rocketTeam['cash'] / (rocketTeam['assets'] + rocketTeam['cash'])
            ratioDiff = bestCashRatio - rocketCashRatio
            if ratioDiff < 0.001 and ratioDiff > -0.001:
                pass
            elif ratioDiff > 0:
                Rocket.sell(ratioDiff * (rocketTeam['assets'] + rocketTeam['cash']) / price)
            else:
                Rocket.buy(- ratioDiff * (rocketTeam['assets'] + rocketTeam['cash']) / price)
    
    Rocket.get(callback)
