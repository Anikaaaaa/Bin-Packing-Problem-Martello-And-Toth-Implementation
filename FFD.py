import os
import time
import csv

def firstFit(weight , capacity):

    res = 0;
    bin = 0

    remainBins = [capacity] * len(weight)


    for i in range( 0 , len(weight)):

        j = 0

        while j < res:

            # print(bin)
            if remainBins[j] >= weight[i]:
                remainBins[j] = remainBins[j] - weight[i]
                break
            j = j + 1

        if j == res:
            remainBins[res] = capacity - weight[i]
            res += 1

    return res

def firstFitDec(weight , capacity):

    weight.sort(reverse=True)

    # print(weight)

    return firstFit(weight,capacity)


def optBenchmark():

    benchMark = {}

    with open("OPT.txt") as my_file:
        for line in my_file:
            line = line.split("\t")
            benchMark[line[0] +".BPP"] = line[1]
            # print(line[0])

    return benchMark



def FFDReader(benchMark):
    all_files = os.listdir("benchmark/")

    rows = []


    for i in range( 0, len(all_files)):

        fileLines = []
        file = "benchmark/"+all_files[i];

        start_time = time.time()

        with open(file) as my_file:
            for line in my_file:
                fileLines.append(line)

        capacity = int( fileLines[1] )
        weight = []
        for elem in range(2 , len(fileLines)):
            weight.append(int(fileLines[elem]))

        requiredBins = firstFitDec(weight,capacity)



        print("FILE NAME : " , all_files[i] , " => REQUIRED BINS : " , requiredBins , " => EXTRA BINS : " , requiredBins - int(benchMark[all_files[i]]),
             " => OPT BINS " ,int(benchMark[all_files[i]]) ," => TIME TAKEN(ms) " , (time.time()  - start_time)*1000.0 )

        temp = []
        temp.append(all_files[i])
        temp.append(str(requiredBins))
        temp.append(str(requiredBins - int(benchMark[all_files[i]])))
        temp.append(str((time.time()  - start_time)*1000.0))

        rows.append(temp)


        CSVprinting(rows , "ffd.csv");



def nextFIT(weight , capacity):

    remainCapacity = capacity;
    res = 0;

    for i in range( 0 , len(weight)):
        if weight[i] > remainCapacity:
            res += 1
            remainCapacity = capacity - weight[i]
        else:
            remainCapacity = remainCapacity - weight[i]

    return res

def nextFitFILE(benchMark):
    all_files = os.listdir("benchmark/")

    rows = []

    for i in range(0, len(all_files)):

        fileLines = []
        file = "benchmark/" + all_files[i];

        start_time = time.time()

        with open(file) as my_file:
            for line in my_file:
                fileLines.append(line)

        capacity = int(fileLines[1])
        weight = []
        for elem in range(2, len(fileLines)):
            weight.append(int(fileLines[elem]))

        requiredBins = nextFIT(weight, capacity)

        temp = []

        print("FILE NAME : " , all_files[i] , " => REQUIRED BINS : " , requiredBins , " => EXTRA BINS : " , requiredBins - int(benchMark[all_files[i]]),
             " => OPT BINS " ,int(benchMark[all_files[i]]) ," => TIME TAKEN(ms) " , (time.time()  - start_time)*1000.0 )

        temp = []
        temp.append(all_files[i])
        temp.append(str(requiredBins))
        temp.append(str(requiredBins - int(benchMark[all_files[i]])))
        temp.append(str((time.time() - start_time) * 1000.0))

        rows.append(temp)

        CSVprinting(rows, "nf.csv");


def CSVprinting(rows , filename):


    fields = ['FILE NAME', 'REQUIRED BINS', 'EXTRA BINS', 'TIME TAKEN(ms)']

    # writing to csv file
    with open(filename, 'w', newline = '') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)



def main():
    benchmark = optBenchmark()
    FFDReader(benchmark)
    nextFitFILE(benchmark)

if __name__ == "__main__":
    main()





