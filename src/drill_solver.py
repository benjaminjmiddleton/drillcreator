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
    scale2 = (max(scale2[0], 1e-100), max(scale2[1], 1e-100))
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
        x += abs(center[0] - p[0]);
        y += abs(center[1] - p[1])
    return (x / len(s), y / len(s))



def getRoughTransition(players, set1, set2):
    """Returns a rough estimation of the transition by applying the translation and scale between the 2 sets to set1 and ranking possible destinations for each player. 
    These destinations are then allocated to minimize overall distance from that rough target set"""
    
    def averagePlace(main, lr, tb):
        weights = [1,1,1]
        return ((main[0]*weights[0] + lr[0]*weights[1] + tb[0]*weights[2])/sum(weights), (main[1]*weights[0] + lr[1]*weights[1] + tb[1]*weights[2])/sum(weights))
                   
    
    s1Average = averageSetCenter(set1);
    s1Scale = averageSetDistance(set1, s1Average);
    
    s1Left = []
    s1Right = []
    s1Top = []
    s1Bottom = [];
    for s in set1:
        if s[0] < s1Average[0]:
            s1Left.append(s);
        else:
            s1Right.append(s);
        if s[1] > s1Average[1]:
            s1Bottom.append(s);
        else:
            s1Top.append(s);
            
            
            
    s1LeftAverage = averageSetCenter(s1Left);
    s1LeftScale = averageSetDistance(s1Left, s1LeftAverage);
    s1RightAverage = averageSetCenter(s1Right);
    s1RightScale = averageSetDistance(s1Right, s1RightAverage);
    s1TopAverage = averageSetCenter(s1Top);
    s1TopScale = averageSetDistance(s1Top, s1Average);
    s1BottomAverage = averageSetCenter(s1Bottom);
    s1BottomScale = averageSetDistance(s1Bottom, s1BottomAverage);
            
    s2Average = averageSetCenter(set2);
    s2Scale = averageSetDistance(set2, s2Average);
    
    s2Left = []
    s2Right = []
    s2Top = []
    s2Bottom = [];
    for s in set2:
        if s[0] < s2Average[0]:
            s2Left.append(s);
        else:
            s2Right.append(s);
        if s[1] > s2Average[1]:
            s2Bottom.append(s);
        else:
            s2Top.append(s);
            
            
    s2LeftAverage = averageSetCenter(s2Left);
    s2LeftScale = averageSetDistance(s2Left, s2LeftAverage);
    s2RightAverage = averageSetCenter(s2Right);
    s2RightScale = averageSetDistance(s2Right, s2RightAverage);
    s2TopAverage = averageSetCenter(s2Top);
    s2TopScale = averageSetDistance(s2Top, s2Average);
    s2BottomAverage = averageSetCenter(s2Bottom);
    s2BottomScale = averageSetDistance(s2Bottom, s2BottomAverage);
    
    candidates = {}
    targets = {}
    for s1 in set1:
        
        translationToCenter1 = subtractCoordinate(s1Average, s1);
        translationFromCenter2 = scaleCoordinate(translationToCenter1, s2Scale, s1Scale);
        mainTarget = subtractCoordinate(s2Average, translationFromCenter2)
        
        s1LRAvereage = s1LeftAverage if s1 in s1Left else s1RightAverage;
        s1LRScale = s1LeftScale if s1 in s1Left else s1RightScale;
        s2LRAvereage = s2LeftAverage if s1 in s1Left else s2RightAverage;
        s2LRScale = s2LeftScale if s1 in s1Left else s2RightScale;
        
        translationToCenter1 = subtractCoordinate(s1LRAvereage, s1);
        translationFromCenter2 = scaleCoordinate(translationToCenter1, s2LRScale, s1LRScale);
        lrTarget = subtractCoordinate(s2LRAvereage, translationFromCenter2)
        
        s1TBAvereage = s1BottomAverage if s1 in s1Bottom else s1TopAverage;
        s1TBScale = s1BottomScale if s1 in s1Bottom else s1TopScale;
        s2TBAvereage = s2BottomAverage if s1 in s1Bottom else s2TopAverage;
        s2TBScale = s2BottomScale if s1 in s1Bottom else s2TopScale;
        
        translationToCenter1 = subtractCoordinate(s1TBAvereage, s1);
        translationFromCenter2 = scaleCoordinate(translationToCenter1, s2TBScale, s1TBScale);
        tbTarget = subtractCoordinate(s2TBAvereage, translationFromCenter2)
        
        target = averagePlace(mainTarget, lrTarget, tbTarget);
        
        
        spots = copy.copy(set2);
        spots.sort(key=lambda x: calculateDistance(target, x));
        

        candidates[s1] = spots;
        targets[s1] = target;
    return targets, candidates
    
    
def alocateTransition(set1, targets, spots):
        oneToTwo = {x: None for x in set1}
        twoToOne = {x: None for x in spots[set1[0]]}
        ranks = {x: 0 for x in set1}
        conflict = None
        
        spotsToAllocate = copy.copy(set1);
        
        spotsToAllocate.sort(key=lambda x: calculateDistance(targets[x], spots[x][0]), reverse=True);
        
        for s in spotsToAllocate:
            conflict = s;
            while(conflict is not None):
                if twoToOne[spots[conflict][ranks[conflict]]] == None:
                    oneToTwo[conflict] = spots[conflict][ranks[conflict]]
                    twoToOne[oneToTwo[conflict]] = conflict;
                    conflict = None
                else:
                    a = conflict;
                    b = twoToOne[spots[s][ranks[s]]];
                    if calculateDistance(a, spots[a][ranks[a]]) - calculateDistance(b, spots[b][ranks[b] + 1]) < calculateDistance(a, spots[a][ranks[a] + 1]) + calculateDistance(b, spots[b][ranks[b]]):                   
                        oneToTwo[a] = oneToTwo[b]
                        oneToTwo[b] = None;
                        ranks[b] += 1;
                        conflict = b;
                        twoToOne[oneToTwo[a]] = a;
                    else:
                        ranks[a] += 1;
                        conflict = a;
                        
        return [oneToTwo[x] for x in set1];    
    
    
def fixTransitions(s1, s2, counts, previousBest = None):
    """Returns set with least amount of collisions obtainable from swapping"""
    
        
    def calculateCollisions(s1, s2, counts):
        """Returns list of collisions as a list of the format [a1,b1,...,an,bn], where adjacent a/b pairs are a the indecies of the players in the collision and every index can only appear once"""
        """Collisions are defined as being within 1 step of another player for 1 count"""
        def updatePlayer(t1, t2, c):
            """Returns set for next count based on linear transitions between sets"""
            return (t1[0] + (t2[0] - t1[0]) / c, t1[1] + (t2[1] - t1[1]) / c)
            
        collisions = [];
        for i in range(counts,0,-1):
            for j in range(len(s1)):
                for k in range(j):
                    d = calculateDistance(s1[j],s1[k])
                    if d < 1:
                        if j not in collisions and k not in collisions:
                            collisions.append(j);
                            collisions.append(k);
                    
            s1 = [updatePlayer(s1[p], s2[p], i) for p in range(min(len(s1),len(s2)))]
        return collisions;
        
    def swap(drillSet, i1, i2):
        """Swaps the elements of drillSet at indexes i1 and i2"""
        temp = drillSet[i1];
        drillSet[i1] = drillSet[i2];
        drillSet[i2] = temp
        return drillSet;
    
    
    collisions = calculateCollisions(s1, s2, counts)
    print(f"COLLISIONS COUNT: {len(collisions) // 2}");
    if len(collisions) == 0:
        print("NO COLLISIONS");
        return s2;
    if previousBest and s2 == previousBest[1]:
        print("COLLISION LOOP DETECTED")
        return s2;
    if previousBest == None or previousBest[0] > len(collisions) // 2:
        previousBest = (len(collisions) // 2, copy.deepcopy(s2))
    for i in range(len(collisions) // 2):
        s2 = swap(s2, collisions[i*2], collisions[i*2 + 1]);
    return fixTransitions(s1, s2, counts, previousBest);

if __name__ == "__main__":  
    players = ["A","B","C","D"] 
    set1 = [(x*4,y*4) for x in range(-4,4) for y in range(5)] # 4 step grid

    """Each line applies a different translation to set2, starting with copying set1"""
    set2 = [x for x in set1] # static set

    #set2 = [(x[0],x[1] + 8) for x in set2] # translation
    #set2 = [(x[0]*2,x[1]*2) for x in set2] # expansion
    #set2 = [(x[1], x[0]) for x  in set2] # rotation
    set2 = [(x[0] - 8 if x[0] < 0 else x[0] + 8, x[1]) for x in set2] # split
    #set2 = [(x[0], x[1] + x[0]/8) for x  in set2] # skew
    print(set1)

    print("CALCULATING ROUGH TRANSITION")
    roughSet, candidates = getRoughTransition(players, set1, set2)
    print("ALLOCATING")
    allocatedSet  = alocateTransition(set1, roughSet, candidates);
    print("RESOLVING COLLISIONS");
    fixedSet = fixTransitions(set1,allocatedSet,8)
    print(fixedSet);