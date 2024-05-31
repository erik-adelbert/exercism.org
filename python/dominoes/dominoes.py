"""
dominoes.py --
solution to https://exercism.org/tracks/python/exercises/dominoes
"""

from collections import defaultdict
from copy import copy


def can_chain(dominoes: list[tuple[int, int]]):
    """
    Determines if a given set of dominoes can be arranged in a chain
    where the ends of adjacent dominoes match.
    Returns a list representing the chain if possible, otherwise returns None.

    Args:
        dominoes (list of tuple): A list of tuples where each tuple represents
        a domino as a pair of integers.

    Returns:
        list of tuple: A list of tuples representing the chain of dominoes if
        possible, otherwise None.
    """
    if not dominoes:
        return []  # an empty chain is valid

    hand = copy(dominoes)  # preserve input

    graph: defaultdict[int, list[int]] = defaultdict(list[int])
    degree: defaultdict[int, int] = defaultdict(int)

    # Build the graph
    for a, b in hand:
        graph[a].append(b)
        graph[b].append(a)
        degree[a] += 1
        degree[b] += 1

    # we're looking for a circuit we can start with the first number on the first domino
    start = next(iter(graph))

    # Check the degrees of vertices
    # if any node has an odd count no euler circuit exists
    if any(v & 1 == 1 for v in degree.values()):
        return None

    # Hierholzer's algorithm to find the Eulerian path/circuit
    def find_eulerian_path(graph: defaultdict[int, list[int]], start: int):
        stack: list[int] = [start]
        path: list[int] = []
        while stack:
            v = stack[-1]
            if graph[v]:
                u = graph[v].pop()
                stack.append(u)
                graph[u].remove(v)
            else:
                path.append(stack.pop())
        return path[::-1]

    epath = find_eulerian_path(graph, start)

    # Check if the path includes all dominoes
    if len(epath) - 1 == len(hand):
        # Reconstruct the domino sequence from the Eulerian path
        return list(zip(epath, epath[1:]))

    return None
