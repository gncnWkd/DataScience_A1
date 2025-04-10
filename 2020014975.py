import sys
from collections import Counter
from itertools import combinations

def count_DB(itemset: tuple, DB: list):   #candidate에 있는 itemset이 DB에 몇 개 있는지 count
    count = 0
    for i in DB:
        if all(item in i for item in itemset):
            count+=1
    return count

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
    numbers = [int(num) for num in line.strip().split('\t')]      
    DB.append(numbers)     # list DB에 transactions이 2차원 리스트 형식으로 저장
    

candidate = set()
frequent = {}
frequentItemsets = []


# Initially, size가 1인 frequent itemsets을 구하기 위해 DB를 Scan
flat = [item for sublist in DB for item in sublist]
for item in flat:
    candidate.add((item,))

for item in candidate:
    temp = round(count_DB(item, DB)/len(DB) * 100, 2)
    if temp >= minSupport:
        frequent[item] = temp

print("DB = ", DB)
print("first candidate = ", candidate)
print("first frequent = ", frequent)



while True:
    n = len(list(frequent.keys())[0])
    print("n = ", n)
    candidate.clear()

    # Generate candidate itemsets fo length (n+1) from frequent itemsets of length (n)
    # frequent itemset(크기 n)에 있는 (n-1)개의 item이 공유되면, 두 itemset을 self-join한다
    for i in range(len(frequent)):
        for j in range(i+1, len(frequent)):
            l1, l2 = list(frequent.keys())[i], list(frequent.keys())[j]
            if l1[:n-1] == l2[:n-1]:
                candidateItem = tuple(sorted(set(l1)|set(l2)))
                subsets = combinations(candidateItem, n)
                # self join한 크기 (n+1)의 itemsets에서 크기가 n인 부분집합이 모두 frequent itemset(크기 n) 안에 있으면 candidate가 됨
                if all(tuple(sorted(sub)) in list(frequent.keys()) for sub in subsets): 
                       candidate.add(candidateItem)

    print(candidate)
    
    # Test the candidates against DB
    frequent.clear()
    for i in candidate:
        temp = round(count_DB(i, DB)/len(DB)*100, 2)
        if temp >= minSupport:
            frequent[i] = temp
            
    print(frequent)
    
    
    if len(candidate) == 0 or frequent == {}:
        break

    






'''
#pruning before generating candidate

#generate candidate itemset
pairs = list(combinations(frequent.keys(), 2))
candidate = {}
for pair in pairs:
    candidate[pair] = round(count_DB(pair, DB)/len(DB)*100, 2)
print("secend candidate = ", candidate)

#pruning after generating candidate
frequent = {}
for key,value in candidate.items():
    if value >= minSupport:
        frequent[key] = value
print("second frequent = ",  frequent)'''