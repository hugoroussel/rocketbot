from __future__ import print_function
import os
import neat
import csv
import pickle

FEE = 0.0001
MA_NUMBER = 1

dataset = []
epoche_number = 0

def import_data(dataset):
    with open('training/data_bs_fat.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            dataset.append(row)

def load_inputs(inputs):
    global epoche_number
    epoche = dataset[epoche_number%len(dataset)]
    for n in range(0,int(len(epoche)/4)):
        inputs.append([float(epoche[n*4]),float(epoche[n*4+1]),float(epoche[n*4+2]),float(epoche[n*4+3]),0.0,0.0])
    epoche_number += 1

def simulate(avg_transactions, trend, genome, config, inputs, log):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    usd = 100000
    btc = 0
    transactions = 0
    penality = 0
    btc_ref = inputs[0][0]
    buy = 0
    sell = 0

    for xi in inputs:
        in_size = len(xi)
        price = xi[0]

        ni = xi.copy()
        ni[0] = (ni[0]/btc_ref -1) * 7
        ni[1] = (ni[1]/btc_ref -1) * 7
        ni[2] = (ni[2]/btc_ref -1) * 7
        ni[3] = (ni[3]/btc_ref -1) * 7
        ni[in_size-2] = usd / 100000.0 - 0.5
        ni[in_size-1] = btc * price / 100000.0 - 0.5
        ni = tuple(ni)

        # print(ni)

        output = net.activate(ni)

        if (output[0] > 0):
            btc += (usd * (output[0]) / price) * (1 - FEE)
            usd -= usd * output[0]
            transactions += 1
            buy += 1
            if output[0]*usd > 0.01:
                penality += 1

        elif (output[0] < 0):
            usd += (btc * -output[0] * price) * (1 - FEE)
            btc -= (btc * -output[0])
            transactions += 1
            sell +=1
            if output[0]*usd > 0.01:
                penality += 1

        if log:
            print('\ninput: ', ni, '- output:',output)
            print('bought:',buy,' - sold:',sell)

    fitness = usd + btc * inputs[len(inputs) - 1][0]

    # forcing transactions
    if transactions < 9:
        fitness -= (9 - transactions) * 10000
    #penalizing abusive behavior
    fitness -= 50 * penality


    genome.fitness = fitness - trend
    avg_transactions += transactions


def eval_genomes(genomes, config):

    inputs = []
    load_inputs(inputs)

    avg_transactions = 0
    trend = (100000 / inputs[0][0]) * inputs[len(inputs) - 1][0]

    for genome_id, genome in genomes:
        simulate(avg_transactions, trend, genome, config, inputs, False)

    avg_transactions /= len(genomes)
    print('Average transactions :', avg_transactions)
    print('Market :', trend)

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    #importing dataset
    import_data(dataset)

    # Run for up to data's epoche generations.
    winner = p.run(eval_genomes, 2*len(dataset)-1) #len(dataset))

    inputs = []
    load_inputs(inputs)
    simulate(0, 0, winner, config, inputs, True)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Store the winner !
    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-v1')
    run(config_path)
