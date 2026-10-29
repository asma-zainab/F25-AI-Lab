graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}
def dls(node, goal, limit, path, graph):
    if node == goal:
        return "FOUND", path

    if limit == 0:
        for n in graph[node]:
            if n not in path:
                return "CUTOFF", None

        return "FAILURE", None

    cutoff_found = False

    for n in graph[node]:
        if n not in path:
            status, result_path = dls(
                n, goal, limit - 1, path + [n], graph
            )

            if status == "FOUND":
                return "FOUND", result_path

            if status == "CUTOFF":
                cutoff_found = True

    if cutoff_found:
        return "CUTOFF", None

    return "FAILURE", None
for limit in range(1, 5):
    status, path = dls("A", "G", limit, ["A"], graph)

    print("Depth Limit:", limit)
    print("Status:", status)
    print("Path:", path)
    print()


print("Test 1: Start equals Goal")
print(dls("A", "A", 2, ["A"], graph))

unreachable_graph = {
    "A": ["B"],
    "B": [],
    "X": []
}
print("\nTest 2: Unreachable Goal")
print(dls("A", "X", 3, ["A"], unreachable_graph))
cycle_graph = {
    "A": ["B"],
    "B": ["A"],
    "X": []
}
print("\nTest 3: Graph with a Cycle")
print(dls("A", "X", 4, ["A"], cycle_graph))
