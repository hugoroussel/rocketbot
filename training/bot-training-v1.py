from __future__ import print_function
import os
import neat

FEE = 0.001

inputs = [(4324.0, 0.0, 0.0), (4532.0, 0.0, 0.0), (4212.0, 0.0, 0.0), (4133.0, 0.0, 0.0)]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        usd = 100000
        btc = 0
        for xi in inputs:
            lst = list(xi)
            lst[1] = usd
            lst[2] = btc
            xi = tuple(lst)
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

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-v1')
    run(config_path)
