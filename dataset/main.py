import csv
import random

data_coinbase = []
data_bitstamp = []


coinbase_filename = "coinbase-1min.csv"
bitstamp_filename = "bitstamp-1min.csv"

output_coinbase = "data_cb.csv"
output_bitstamp = "data_bs.csv"

#last 200, 1000

EPOCHS = 200
EPOCH_TIME = 1000

N1 = 5
N2 = 10
N3 = 20







def readData(input_file, list):
    with open(input_file, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if (row[7] != "Weighted_Price" and row[7] != 'NaN' and row[7] != ""):
                list.append([float(row[7]) ])

def takeRandomSlice(output_file, list):
    with open(output_file, 'w') as f:
        for i in range(0, EPOCHS):
            randomStart = random.randrange(1, len(list))
            for item in list[randomStart:randomStart + EPOCH_TIME]:
                f.write("%s," % item[0])
            f.write("\n")


def writeAndMA(output_file, list):
    with open(output_file, 'w') as f:
        for i in range(0, EPOCHS):
            runSum1, running_aves1 = [0], []
            runSum2, running_aves2 = [0], []
            runSum3, running_aves3 = [0], []
            randomStart = random.randrange(1, len(list))
            for i, item in enumerate(list[randomStart:randomStart + EPOCH_TIME],1):
                runSum1.append(runSum1[i-1]+item[0])
                runSum2.append(runSum2[i - 1] + item[0])
                runSum3.append(runSum3[i-1]+item[0])
                if i>=N3:
                    moving_ave1 = (runSum1[i] - runSum1[i - N1]) / N1
                    moving_ave2 = (runSum2[i] - runSum2[i - N2]) / N2
                    moving_ave3 = (runSum3[i] - runSum3[i - N3]) / N3
                    f.write("%s," % item[0])
                    f.write("%s," % moving_ave1)
                    f.write("%s," % moving_ave2)
                    f.write("%s," % moving_ave3)
                    running_aves1.append(moving_ave1)
                    running_aves2.append(moving_ave2)
                    running_aves3.append(moving_ave3)

            f.write("\n")



def writeToFile(list):
    with open('data.txt', 'w') as f:
        for item in list:
            f.write("%s\n" % item)




readData(coinbase_filename, data_coinbase)
readData(bitstamp_filename, data_bitstamp)
print("Data was read correctly")
print("Data points from coinbase: %u" % len(data_coinbase))
print("Data points from bitstamp: %u" % len(data_bitstamp))

writeAndMA(output_coinbase,data_coinbase)
writeAndMA(output_bitstamp,data_bitstamp)
print("done")

















