from __future__ import print_function
import os
import neat
import csv
import pickle

FEE = 0.00001

dataset = []
epoche_number = 0

def import_data(dataset):
    with open('training/data.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            dataset.append(row)

def load_inputs(inputs):
    global epoche_number
    for n in dataset[epoche_number]:
        if(n != ''):
            inputs.append([float(n),0.0,0.0])
    epoche_number += 1

def eval_genomes(genomes, config):

    inputs = []
    load_inputs(inputs)

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        usd = 100000
        btc = 0
        for xi in inputs:
            xi[1] = usd
            xi[2] = btc
            xi = tuple(xi)
            output = net.activate(xi)

            if output[0] > 0.8:
                btc += (usd / xi[0]) * (1 - FEE)
                usd = 0
            elif output[0] < 0.2:
                usd += (btc * xi[0]) * (1 - FEE)
                btc = 0

        usd += btc * inputs[len(inputs) - 1][0]
        genome.fitness = usd

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
