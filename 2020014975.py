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
    line = line.rstrip("\n")        # line의 끝에 붙어있는 \n 제거 
    DB.append(line.split("\t"))     # list DB에 transactions이 2차원 리스트 형식으로 저장
    


