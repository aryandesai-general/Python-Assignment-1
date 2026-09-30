"""Q6: Lexicographically smallest module loading order; detect dependency cycles."""
import heapq
import sys
from collections import defaultdict


def main():
    try:
        n, e = map(int, sys.stdin.readline().split())
        if n < 1 or e < 0:
            raise ValueError
        modules = [sys.stdin.readline().strip() for _ in range(n)]
        if any(not name for name in modules) or len(set(modules)) != n:
            raise ValueError
        known = set(modules)
        graph = defaultdict(list)
        indegree = {name: 0 for name in modules}
        for _ in range(e):
            line = sys.stdin.readline().split()
            if len(line) != 3 or line[1] != "imports":
                raise ValueError
            importer, dependency = line[0], line[2]
            if importer not in known or dependency not in known:
                raise ValueError
            # dependency must load before importer; ignore duplicate edges.
            edge = (dependency, importer)
            if importer not in graph[dependency]:
                graph[dependency].append(importer)
                indegree[importer] += 1
    except ValueError:
        print("Invalid input.")
        return

    ready = [name for name, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        current = heapq.heappop(ready)
        order.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                heapq.heappush(ready, neighbor)

    if len(order) == n:
        print(*order)
    else:
        remaining = sorted(name for name, degree in indegree.items() if degree > 0)
        print("CYCLE")
        print(*remaining)


if __name__ == "__main__":
    main()
