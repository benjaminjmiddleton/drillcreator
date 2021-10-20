def distance(pt0: tuple[float, float], pt1: tuple[float, float]) -> float:
    """Computes the distance between two points"""
    return abs(((pt0[0] - pt1[0]) * (pt0[0] - pt1[0])) + ((pt0[1] - pt1[1]) * (pt0[1] - pt1[1])))

def getMatrixPermutations(set0: tuple[tuple[float, float], ...],
                          set1: tuple[tuple[float, float], ...],
                          cutoff: float) -> tuple[tuple[float, float, float], ...]:
    """Let's try something"""

    # First let's validate our inputs
    assert(set0.count == set1.count)
    assert(cutoff >= 0)

    # Now we'll build our matrix (just using lists for now, may consider something more optimal in the future)
    matrix = []
    for start in set0:
        rows = []
        for end in set1:
            rows.append(distance(start, end))
        matrix.append(rows)
