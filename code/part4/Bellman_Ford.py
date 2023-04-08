from SPAlgorithm import SPAlgorithm

class Bellman_Ford(SPAlgorithm):
    
    def calc_sp(self, graph, source, dest):
        return self.bellman_ford(graph, source)[dest]


    def bellman_ford(self, G, source):
        pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {} #Distance dictionary
        nodes = list(G.adj.keys())

        #Initialize distances
        for node in nodes:
            dist[node] = float("inf")
        dist[source] = 0

        #Meat of the algorithm
        for _ in range(G.number_of_nodes()):
            for node in nodes:
                for neighbour in G.adj[node]:
                    if dist[neighbour] > dist[node] + G.w(node, neighbour):
                        dist[neighbour] = dist[node] + G.w(node, neighbour)
                        pred[neighbour] = node
        return dist

