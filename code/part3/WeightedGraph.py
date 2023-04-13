class WeightedGraph():

    def __init__(self):
        self.adj = {}
        self.weights = {}
        self.lines = {}

    def get_adj_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight, line):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        if node1 not in self.adj[node2]:
            self.adj[node2].append(node1)
        self.weights[(node1, node2)] = weight
        self.weights[(node2, node1)] = weight
        self.lines[(node1, node2)] = line
        self.lines[(node2, node1)] = line

    def get_num_of_nodes(self):
        return len(self.adj)

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def l(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.lines[(node1, node2)]

    def are_connected(self, node1, node2):  # IDK if we're allowed to keep this
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False
