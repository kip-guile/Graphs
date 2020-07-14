from queue import Queue


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)


def earliest_ancestor(ancestors, starting_node):
    graph = Graph()

    for ancestor in ancestors:
        graph.add_vertex(ancestor[0])
        graph.add_vertex(ancestor[1])
    for ancestor in ancestors:
        graph.add_edge(ancestor[1], ancestor[0])

    q = Queue()
    q.enqueue([starting_node])

    max_path_length = 1
    earliest_ancestor = -1

    while q.size() > 0:
        path = q.dequeue()
        vertex = path[-1]

        if (len(path) >= max_path_length and vertex < earliest_ancestor) or (len(path) > max_path_length):
            earliest_ancestor = vertex
            max_path_length = len(path)

        for neighbor in graph.vertices[vertex]:
            new_path = list(path)
            new_path.append(neighbor)
            q.enqueue(new_path)
    return earliest_ancestor
