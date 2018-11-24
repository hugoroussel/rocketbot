from Rocket import *

print('# Rocket exemples')
print()

print('## Launching a BUY order')
Rocket.buy(1)
print()

print('## Launching a SELL order')
Rocket.sell(1)
print()

print('## Getting the team')
print(Rocket.team())
print()

print('## Getting the transactions array')
print(Rocket.transactions())
print()

print('## Getting the live price')
# the `print` method here is the method called for each new price
Rocket.get(print)
