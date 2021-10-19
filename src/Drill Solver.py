import copy

def calculateDistance(a,b):
    """Return distance between 2-tuples a and b"""
    return ((b[0] - a[0])**2 + (b[1] - a[1])**2)**.5
   
def addCoordinates(a, b):
    """Return 2-tuple sum of elements for 2-tuples a and b"""
    return (a[0] + b[0], a[1] + b[1])
    
def subtractCoordinate(a,b):
    """Return 2-tuple difference of elements for 2-tuples a and b"""
    return (a[0] - b[0], a[1] - b[1])
    
def scaleCoordinate(a, scale1, scale2):
    """Returns scaled 2-tuple based of x and y scales initial and final scales, given as 2-tuples"""
    return (a[0]*scale1[0]/scale2[0], a[1]*scale1[1]/scale2[1])
    
def averageSetCenter(s):
    """Returns the average location of a list of 2-tuples as a 2-tuple"""
    x = s[0][0]
    y = s[0][1]
    
    for i in range(1, len(s)):
        x += s[i][0]
        y += s[i][1]
    return (x/len(s), y/len(s));
    
def averageSetDistance(s, center):
    """Returns the average distance of the 2-tuple elements of a list s from the 2-tuple center in both the x and y directions as a 2-tuple (xScale, uScale)"""
    x = 0;
    y = 0;
    for p in s:
        x = abs(center[0] - p[0]);
        y = abs(center[1] - p[1])
    return (x / len(s), y / len(s))



def getPermutations(players, set1, set2):
    """Returns all not obviously wrong transitions between lists of 2-tuples set1 and set2 as a list, players currently unused
    Each result in list will be a permutation of set2 where the index corresponds to the same index in set1"""

    def check(targetSet, possibilities):
        """Checks to make sure all elements in targetSet appear at least once, returns true if all elements are present else false"""
        for s in targetSet:
            isPresent = False;
            for p in possibilities:
                if s in p:
                    isPresent = True;
                    break;
            if (isPresent):
                continue;
            return 0;
        return 1;
                   
        
    
    def permutate(steps, permutations = []):
        """Returns list of all permutations from a list of lists which consist of the valid destinations of each marcher represented as 2-tuples
        Removes elements that have repeats"""
        
        if len(steps) == 0:
            return permutations
        if len(permutations) == 0:
            target = steps[0]
            steps.remove(target)
            return permutate(steps, [[x] for x in target])
        result = [];
        target = steps[0]
        steps.remove(target)
        for p in permutations:
            for s in target:
                if s not in p:
                    newP = copy.deepcopy(p)
                    newP.append(s)
                    result.append(newP)
        print(len(result))
        return permutate(steps, result)
    
    distances = [];
    for s1 in set1:
        for s2 in set2:
            distances.append(calculateDistance(s1,s2));
    
    mean = sum(distances) / len(distances)
    std = (sum([((x - mean)**2) for x in distances]) / len(distances))**.5
    
    s1Average = averageSetCenter(set1);
    s1Scale = averageSetDistance(set1, s1Average);
    s2Average = averageSetCenter(set2);
    s2Scale = averageSetDistance(set2, s2Average);
    
    candidates = {}
    possibilities = [];
    for s1 in set1:
        
        translationToCenter1 = subtractCoordinate(s1Average, s1);
        translationFromCenter2 = scaleCoordinate(translationToCenter1, s2Scale, s1Scale);
        target = subtractCoordinate(s2Average, translationFromCenter2)
        
        spots = copy.copy(set2);
        
        spots.sort(key=lambda x: calculateDistance(target, x));
        
        candidates[s1] = spots;
        maxDistance = calculateDistance(target, spots[0])
        firstOut = 1;
        while(firstOut < len(spots) and calculateDistance(target, spots[firstOut]) < max(4,maxDistance*1.5)):
            firstOut += 1;
        temp = spots[:firstOut*2];
        possibilities.append(temp)   
    
    return permutate(possibilities)
    
    
def rankTransition(s1, s2, counts):
    """Returns score for transition from lists of 2-tuples set1 and set2 in an integer number of counts where 0 is best"""
    
        
    def calculateCollisions(s1, s2, counts):
        """Returns the number of collisions during transition, defined as being within 1 step of another player for 1 count"""
        def updatePlayer(t1, t2, c):
            """Returns set for next count based on linear transitions between sets"""
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
    score = distance / len(s1) + maxDistance + collisions*1000000
    return (score, s2)

players = ["A","B","C","D"] 
set1 = [(x*8,y*8) for x in range(0, 2) for y in range(2)] # 8 step grid

"""Each line applies a different translation to set2, starting with copying set1"""
set2 = [x for x in set1] # static set

set2 = [(x[0],x[1] + 8) for x in set2] # translation
#set2 = [(x[0]*1.2,x[1]*1.2) for x in set2] # expansion
#set2 = [(x[1], x[0]) for x  in set2] # rotation
#set2 = [(x[0] - 8 if x[0] < 0 else x[0] + 8, x[1]) for x in set2] # split
#set2 = [(x[0], x[1] + x[0]/8) for x  in set2] # skew

print("PERMUTATING")
p = getPermutations(players, set1, set2)
print("CALCULATING SCORES");
rankings = [rankTransition(set1,s2,8) for s2 in p]
print("SORTING RANKINGS")
rankings.sort(key=lambda tup: tup[0])

for r in rankings[:10]:
    print(r)
