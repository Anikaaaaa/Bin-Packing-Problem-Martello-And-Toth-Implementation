import os
import time
import csv
import math


class Node:
    def __init__(self, wRemaining, level, numBoxes):
        self.wRemaining = wRemaining  # array of remaining weight for each box
        self.level = level  # the level of the node in branch and bound tree
        self.numBoxes = numBoxes  # number of used boxes

    def getLevel(self):
        return self.level

    def getNumberBoxes(self):
        return self.numBoxes

    def getWRemainings(self):
        return self.wRemaining

    def getWRemaining(self, i):
        return self.wRemaining[i]

def firstFit(weight , capacity):

    res = 0

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

def L1_Bound(weights, capacity):
    return math.ceil(1.0 * sum(weights) / capacity)

# branch and bound bin packing exact algorithm
def branchAndBound(n, c, w):

    minBoxes = n  # initialize the number of used boxes
    minBoxes = firstFitDec(w, c)
    Nodes = []  # array contains the unprocessed nodes
    # array contains remaining weight in each box [c,c,c,.......c]
    wRemaining = [c]*n
    numBoxes = 0  # initialise number of used boxes
    lowerBound = L1_Bound(w, c)
    print('Lower Bound --> ' + str(lowerBound))

    # create the root node, level 0, number of used boxes 0
    curN = Node(wRemaining, 0, numBoxes)

    Nodes.append(curN)  # add the root node to Nodes

    while len(Nodes) > 0:  # As long as Nodes is not empty do

        curN = Nodes.pop()  # get a node to process it : curent node (curN)
        curLevel = curN.getLevel()  # get the level of curN

        # if this node is a leaf of the tree and the number of used boxes < minBoxes
        if (curLevel == n) and (curN.getNumberBoxes() < minBoxes):
            minBoxes = curN.getNumberBoxes()  # update minBoxes
        
        if curLevel == n and curN.getNumberBoxes() == lowerBound:
            return lowerBound

        else:
            indNewBox = curN.getNumberBoxes()

            # else, if from this node the number of used boxes < minBoxes (not dominated)
            if (indNewBox < minBoxes):

                wCurLevel = w[curLevel]
                # we will try to add the following item in each box already used, and in a new box (that's why I added +1 to indNewBox)
                for i in range(indNewBox+1):

                    # if it is possible to add the item in the box i (weight remaining in the box > weight of the item)
                    if (curLevel < n) and (curN.getWRemaining(i) >= wCurLevel):
                        # we will create a node and add it to Nodes.
                        newWRemaining = curN.getWRemainings()[:]
                        # remaining weight in box i - weight of the item to be added
                        newWRemaining[i] -= wCurLevel

                        if (i == indNewBox):  # new Box
                            newNode = Node(
                                newWRemaining, curLevel + 1, indNewBox + 1)
                        else:  # already used box
                            newNode = Node(
                                newWRemaining, curLevel + 1, indNewBox)

                        Nodes.append(newNode)

    return minBoxes


def branchAndBoundFILE(benchMark):
    all_files = sorted(os.listdir("benchmark/"))

    rows = []

    for i in range(0, len(all_files)):

        fileLines = []
        file = "benchmark/" + all_files[i]

        start_time = time.time()

        with open(file) as my_file:
            for line in my_file:
                fileLines.append(line)

        n_items = int(fileLines[0])
        capacity = int(fileLines[1])
        weight = []
        for elem in range(2, len(fileLines)):
            weight.append(int(fileLines[elem]))

        #weight = np.array(weight)
        requiredBins = branchAndBound(n_items, capacity, weight)

        temp = []

        print("FILE NAME : ", all_files[i], " => REQUIRED BINS : ", requiredBins, " => EXTRA BINS : ", requiredBins - int(benchMark[all_files[i]]),
              " => OPT BINS ", int(benchMark[all_files[i]]), " => TIME TAKEN(ms) ", (time.time() - start_time)*1000.0)

        temp = []
        temp.append(all_files[i])
        temp.append(str(requiredBins))
        temp.append(str(requiredBins - int(benchMark[all_files[i]])))
        temp.append(str((time.time() - start_time) * 1000.0))

        rows.append(temp)

        CSVprinting(rows, "bnb.csv")


def CSVprinting(rows, filename):

    fields = ['FILE NAME', 'REQUIRED BINS', 'EXTRA BINS', 'TIME TAKEN(ms)']

    # writing to csv file
    with open(filename, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


def optBenchmark():

    benchMark = {}

    with open("OPT.txt") as my_file:
        for line in my_file:
            line = line.split("\t")
            benchMark[line[0] + ".BPP"] = line[1]
            # print(line[0])

    return benchMark


def main():
    benchmark = optBenchmark()
    branchAndBoundFILE(benchmark)


if __name__ == "__main__":
    main()
