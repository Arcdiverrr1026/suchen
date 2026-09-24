"""Social network model with an undirected graph.

Command line input format:
    n m
    person_1
    ...
    person_n
    person_a person_b
    ... m lines
    start end

Output is the shortest connection path, or "No connection".
"""

from collections import deque
from dataclasses import dataclass, field


@dataclass
class SocialNetwork:
    adjacency: dict[str, set[str]] = field(default_factory=dict)

    def add_person(self, name: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("person name cannot be empty")
        self.adjacency.setdefault(name, set())

    def add_acquaintance(self, left: str, right: str) -> None:
        self.add_person(left)
        self.add_person(right)
        self.adjacency[left].add(right)
        self.adjacency[right].add(left)

    def shortest_connection(self, start: str, end: str) -> list[str]:
        if start not in self.adjacency or end not in self.adjacency:
            return []
        if start == end:
            return [start]

        queue: deque[str] = deque([start])
        previous: dict[str, str | None] = {start: None}

        while queue:
            current = queue.popleft()
            for neighbor in sorted(self.adjacency[current]):
                if neighbor in previous:
                    continue
                previous[neighbor] = current
                if neighbor == end:
                    return self._build_path(previous, end)
                queue.append(neighbor)

        return []

    @staticmethod
    def _build_path(previous: dict[str, str | None], end: str) -> list[str]:
        path: list[str] = []
        current: str | None = end
        while current is not None:
            path.append(current)
            current = previous[current]
        return list(reversed(path))


def _read_pair(line: str) -> tuple[str, str]:
    parts = line.strip().split()
    if len(parts) != 2:
        raise ValueError("expected two names separated by spaces")
    return parts[0], parts[1]


def main() -> None:
    n, m = map(int, input().split())
    network = SocialNetwork()

    for _ in range(n):
        network.add_person(input().strip())
    for _ in range(m):
        left, right = _read_pair(input())
        network.add_acquaintance(left, right)

    start, end = _read_pair(input())
    path = network.shortest_connection(start, end)
    print(" -> ".join(path) if path else "No connection")


if __name__ == "__main__":
    main()
