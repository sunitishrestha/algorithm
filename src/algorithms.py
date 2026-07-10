"""Event-based DFS and BFS component traversals for animation."""


def traversal_events(matrix: list[list[int]], algorithm: str) -> list[dict]:
    """Produce small traversal events so the UI can animate them."""
    n = len(matrix)
    discovered = [False] * n
    events = []
    component = 0
    for start in range(n):
        if discovered[start]:
            continue
        discovered[start] = True
        container = [start]
        events.append({"kind": "component", "vertex": start, "component": component})
        events.append({"kind": "frontier", "vertex": start, "component": component})
        while container:
            vertex = container.pop() if algorithm == "DFS" else container.pop(0)
            events.append({"kind": "visit", "vertex": vertex, "component": component})
            order = range(n - 1, -1, -1) if algorithm == "DFS" else range(n)
            for neighbor in order:
                if matrix[vertex][neighbor]:
                    events.append({"kind": "edge", "source": vertex, "target": neighbor, "component": component})
                    if not discovered[neighbor]:
                        discovered[neighbor] = True
                        container.append(neighbor)
                        events.append({"kind": "frontier", "vertex": neighbor, "component": component})
            events.append({"kind": "done", "vertex": vertex, "component": component})
        component += 1
    events.append({"kind": "finished", "components": component})
    return events
