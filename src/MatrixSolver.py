def getMatrixPermutations(set0: tuple[tuple[float, float], ...],
                          set1: tuple[tuple[float, float], ...],
                          cutoff: float) -> tuple[tuple[float, float, float], ...]:
    """Let's try something"""

    # First let's validate our inputs and get the count
    assert(set0.count == set1.count)
    assert(cutoff >= 0)
    nPoints = set0.count
