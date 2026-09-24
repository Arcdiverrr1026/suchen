"""Simple version: social network shortest connection."""

from collections import deque

n, m = map(int, input().split())
graph = {}

for _ in range(n):
    name = input().strip()
    graph[name] = []

for _ in range(m):
    a, b = input().split()
    graph[a].append(b)
    graph[b].append(a)

start, end = input().split()
queue = deque([start])
visited = {start}
previous = {start: None}

while queue:
    person = queue.popleft()
    if person == end:
        break

    for friend in graph[person]:
        if friend not in visited:
            visited.add(friend)
            previous[friend] = person
            queue.append(friend)

if end not in previous:
    print("No connection")
else:
    path = []
    person = end
    while person is not None:
        path.append(person)
        person = previous[person]
    path.reverse()
    print(" -> ".join(path))
