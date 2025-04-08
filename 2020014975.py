import sys
from collections import Counter
from itertools import combinations


minSupport = int(sys.argv[1])
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
    

candidate = {}
frequent = {}
frequentItemsets = []


# Initially, size가 1인 frequent itemsets을 구하기 위해 DB를 Scan
flat = [item for sublist in DB for item in sublist]
counter = Counter(flat)
for key in sorted(counter):
    candidate[key] = round(counter[key]/len(DB) * 100, 2)
#print(Candidate)

for key,value in candidate.items():
    if value >= minSupport:
        frequent[key] = value

print(candidate)
print(frequent)
print(DB)


def count(itemset: tuple, DB: list):
    count = 0
    for i in len(DB):
        if all(item in DB for item in itemset):
            count+=1
    return count




#while True:
pairs = list(combinations(frequent.keys(), 2))
print(pairs)
candidate = {}
for pair in pairs:
    candidate[pair] = 0