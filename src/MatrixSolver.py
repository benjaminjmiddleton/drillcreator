def distance(pt0: tuple[float, float], pt1: tuple[float, float]) -> float:
    """Computes the distance between two points"""
    return abs(((pt0[0] - pt1[0]) * (pt0[0] - pt1[0])) + ((pt0[1] - pt1[1]) * (pt0[1] - pt1[1])))

def getMatrixPermutations(set0: tuple[tuple[float, float], ...],
                          set1: tuple[tuple[float, float], ...],
                          cutoff: float) -> tuple[tuple[int, ...], ...]:
    """Let's try something"""

    def findPermutations(matrix: tuple[tuple[float, ...], ...],
                         path: tuple[int, ...],
                         maxDist: float,
                         minDist: float,
                         cutoff: float) -> tuple[tuple[int, ...], ...]:
        """Recursive function to find the permutations"""

        # Handle our return condition or set the output
        if matrix == ():
            return (path,)
        output = tuple[tuple[int, ...], ...]()

        # Loop through the distances and compute possible paths
        for idx in range(len(matrix[0])):
            # If we've already selected this spot, continue on
            if idx in path:
                continue
            curDist = matrix[0][idx]

            # Check if the currently indexed value fits within our cutoff
            if curDist > maxDist:
                if abs(curDist - minDist) <= cutoff:
                    output += findPermutations(matrix[1:], path + (idx,), curDist, minDist, cutoff)
            elif curDist < minDist:
                if abs(maxDist - curDist) <= cutoff:
                    output += findPermutations(matrix[1:], path + (idx,), maxDist, curDist, cutoff)
            else:
               output += findPermutations(matrix[1:], path + (idx,), maxDist, minDist, cutoff)

        # Return the final paths
        return output

    # First let's validate our inputs
    assert(len(set0) == len(set1))
    assert(cutoff >= 0)

    # Now we'll build our matrix (just using tuples for now, may consider something more optimal in the future)
    matrix = list[tuple[float, ...]]()
    for start in set0:
        rows = list[float]()
        for end in set1:
            rows.append(distance(start, end))
        matrix.append(tuple(rows))
    matrix = tuple(matrix)

    # Compute the permutations
    output = tuple[tuple[int, ...], ...]()
    for idx in range(len(matrix[0])):
        curDist = matrix[0][idx]
        output += findPermutations(matrix[1:], (idx,), curDist, curDist, cutoff)
    return output

players = ["A","B","C","D"] 
set1 = [(x*8.0,y*8.0) for x in range(0, 2) for y in range(2)] # 8 step grid

"""Each line applies a different translation to set2, starting with copying set1"""
set2 = [x for x in set1] # static set

set2 = [(x[0],x[1] + 8.0) for x in set2] # translation
#set2 = [(x[0]*1.2,x[1]*1.2) for x in set2] # expansion
#set2 = [(x[1], x[0]) for x  in set2] # rotation
#set2 = [(x[0] - 8 if x[0] < 0 else x[0] + 8, x[1]) for x in set2] # split
#set2 = [(x[0], x[1] + x[0]/8) for x  in set2] # skew

print(getMatrixPermutations(tuple(set1), tuple(set2), 1))
