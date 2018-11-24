from __future__ import print_function
import os
import neat
import csv
import pickle

FEE = 0.00001
MA_NUMBER = 1

dataset = []
epoche_number = 0

def import_data(dataset):
    with open('training/data_bs.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            dataset.append(row)

def load_inputs(inputs):
    global epoche_number
    epoche = dataset[epoche_number]
    for n in range(0,int(len(epoche)/2)):
        if(epoche[n*2] != '' and epoche[n*2+1] != ''):
            inputs.append([float(epoche[n*2]),float(epoche[n*2+1]),0.0,0.0])
    epoche_number += 1

def eval_genomes(genomes, config):

    inputs = []
    load_inputs(inputs)

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        usd = 100000
        btc = 0
        transactions = 0
        penalty = 0

        trend = (usd / inputs[0][0]) * inputs[len(inputs) - 1][0]

        for xi in inputs:
            in_size = len(xi)
            price = xi[0]

            ni = xi.copy()
            ni[0] /= 5000.0
            ni[1] /= 5000.0
            ni[in_size-2] = usd / 100000.0
            ni[in_size-1] = btc / 25.0
            ni = tuple(ni)
            output = net.activate(ni)

            if (output[0] > 0.5 and output[1] > 0.5):
                if(usd == 0):
                    penalty += 1
                else:
                    btc += (usd / price) * (1 - FEE)
                    usd = 0
                    transactions += 1
            elif (output[0] < 0.5 and output[1] > 0.5):
                if(btc == 0):
                    penalty += 1
                else:
                    usd += (btc * price) * (1 - FEE)
                    btc = 0
                    transactions += 1

        usd += btc * inputs[len(inputs) - 1][0]
        fitness = usd

        # forcing transactions
        if transactions < 5:
            fitness -= (5 - transactions) * 5000

        fitness -= (penalty * 1000)
        genome.fitness = fitness

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
    winner = p.run(eval_genomes, 10) #len(dataset))

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
