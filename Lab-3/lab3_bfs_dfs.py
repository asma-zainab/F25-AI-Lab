graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}
def bfs(start, goal):
    queue = [(start, [start])]
    seen = [start]
    order = []

    while queue:
        node, path = queue.pop(0)
        order.append(node)

        if node == goal:
            return path, order

        for n in graph[node]:
            if n not in seen:
                seen.append(n)
                queue.append((n, path + [n]))

    return None, order
def dfs(start, goal):
    stack = [(start, [start])]
    seen = []
    order = []

    while stack:
        node, path = stack.pop()

        if node in seen:
            continue

        seen.append(node)
        order.append(node)

        if node == goal:
            return path, order

        for n in reversed(graph[node]):
            if n not in seen:
                stack.append((n, path + [n]))

    return None, order

path, order = bfs("A", "G")
print("BFS Path:", path)
print("BFS Visit Order:", order)

path, order = dfs("A", "G")
print("DFS Path:", path)
print("DFS Visit Order:", order)