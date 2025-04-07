import sys

minSupport = sys.argv[1]
inputFileName = sys.argv[2]
outputFileName = sys.argv[3]

inputFile = open(inputFileName, 'r')
outputFile = open(outputFileName, 'w')

DB = []

while True: 
    line = inputFile.readline()
    if not line:
        break
    line = line.rstrip("\n")
    DB.append(line.split("\t"))
    


