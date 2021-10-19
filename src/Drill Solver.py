import copy

def calculateDistance(a,b):
        return ((b[0] - a[0])**2 + (b[1] - a[1])**2)**.5

def getPermutations(players, set1, set2):
    
    def permutate(steps, permutations = []):
        
        if len(steps) == 0:
            return permutations
        if len(permutations) == 0:
            return permutate(steps[1:], [[x] for x in steps[0]])
        result = [];
        for p in permutations:
            for s in steps[0]:
                if s not in p:
                    newP = copy.deepcopy(p)
                    newP.append(s)
                    result.append(newP)
        return permutate(steps[1:], result)
    
    distances = [];
    for s1 in set1:
        for s2 in set2:
            distances.append(calculateDistance(s1,s2));
    
    mean = sum(distances) / len(distances)
    std = (sum([((x - mean)**2) for x in distances]) / len(distances))**.5
        
    possibilities = [];
    
    for s1 in set1:
        possibilities.append([s2 for s2 in set2 if calculateDistance(s1, s2) < mean + std])
        
    return permutate(possibilities)
    
    
def rankTransition(s1, s2, counts):
    
        
    def calculateCollisions(s1, s2, counts):
        def updatePlayer(t1, t2, c):
            return (t1[0] + (t2[0] - t1[0]) / c, t1[1] + (t2[1] - t1[1]) / c)
            
        collisionCount = 0
        for i in range(counts,0,-1):
            for j in range(len(s1)):
                for k in range(j):
                    d = calculateDistance(s1[j],s1[k])
                    if d < 1:
                        collisionCount += 1;
                    
            s1 = [updatePlayer(s1[p], s2[p], i) for p in range(min(len(s1),len(s2)))]
        return collisionCount;
        
    distance = 0
    maxDistance = 0    
    for i in range(min(len(s1), len(s2))):
        d = calculateDistance(s1[i], s2[i])
        distance += d
        maxDistance = max(d, maxDistance)
    collisions = calculateCollisions(s1, s2, counts)
    score = distance + maxDistance**2 + collisions*100
    return (score, s2)

players = ["A","B","C","D"]  
set1 = [(0,0),(8,0),(0,8),(8,8)]
set2 = [x for x in set1] # static set
#set2 = [(x[0],x[1] + 8) for x in set1] # translation


rankings = [rankTransition(set1,s2,8) for s2 in getPermutations(players, set1, set2)]
rankings.sort(key=lambda tup: tup[0])

for r in rankings:
    print(r)