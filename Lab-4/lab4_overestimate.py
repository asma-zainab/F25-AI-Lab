def astar(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]
    best = {start: 0}
    trace = []
    expanded = 0
    while pq:
        pq.sort()
        f, g, node, path = pq.pop(0)

        if g != best[node]:
            continue

        trace.append(node)

        if node == goal:
            return g, path, trace, expanded

        expanded = expanded + 1

        for nxt, w in graph[node]:
            ng = g + w

            if ng < best.get(nxt, 999999):
                best[nxt] = ng
                pq.append((ng + h[nxt], ng, nxt, path + [nxt]))

    return -1, [], trace, expanded
graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}
h = {
    "S": 5,
    "A": 4,
    "B": 4,
    "C": 10,
    "G": 0
}
print("Overestimate Result:")
print(astar(graph, h, "S", "G"))