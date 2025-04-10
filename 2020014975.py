import sys
from itertools import combinations, chain


def count_DB(itemset, DB: list):   # candidate에 있는 itemset이 DB에 몇 개 있는지 count
    count = 0
    for i in DB:
        if all(item in i for item in itemset):
            count+=1
    return count

def getSubset(itemset: tuple):    # itemset의 자기 자신을 제외한 subset 리스트를 반환
    subsets_tuple = list(chain.from_iterable(combinations(itemset, r) for r in range(1, len(itemset))))
    return [set(c) for c in subsets_tuple]

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

if len(frequent)==0:
    quit()

while True:
    n = len(list(frequent.keys())[0])
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
    
    # Test the candidates against DB
    frequent.clear()
    for i in candidate:
        temp = round(count_DB(i, DB)/len(DB)*100, 2)
        if temp >= minSupport:
            frequent[i] = temp    
    
    # Terminate when no frequent or candidate set can be generated
    if len(candidate) == 0 or len(frequent) == 0:
        break
    
    # frequentItemsets에 길이 2 이상의 frequent itemset들을 모두 저장
    for i in frequent:
        frequentItemsets.append(set(i))    

# output 파일에 item_set, associative_item_set, support,confidence 출력
for itemset in frequentItemsets:
    subsets = getSubset(itemset)

    for base_item_set in subsets:
        associative_item_set = itemset - base_item_set
        support_itemset = round(count_DB(itemset, DB)/len(DB)*100, 2)
        support_base_item_set = round(count_DB(base_item_set, DB)/len(DB)*100, 2)
        if support_base_item_set == 0:
            continue
        confidence = round(support_itemset/support_base_item_set*100, 2)

        data = str(base_item_set) + "\t" + str(associative_item_set) + "\t" + f"{support_itemset:.2f}" + "\t" + f"{confidence:.2f}" + "\n"
        outputFile.write(data)