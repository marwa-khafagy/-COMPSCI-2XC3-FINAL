from SPAlgorithm import SPAlgorithm
import min_heap

class Bellman_Ford(SPAlgorithm):
    
    def calc_sp(self, graph, source, dest):
        return self.dijkstra(graph, source)[dest]


    def dijkstra(G, source):
        pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {} #Distance dictionary
        Q = min_heap.MinHeap([])
        nodes = list(G.adj.keys()) #NO WAY TO GET NODES OTHERWISE

        #Initialize priority queue/heap and distances
        for node in nodes:
            Q.insert(min_heap.Element(node, float("inf")))
            dist[node] = float("inf")
        Q.decrease_key(source, 0)

        #Meat of the algorithm
        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value
            dist[current_node] = current_element.key
            
            # SWITCH METHOD TO COMPLY WITH UML
            for neighbour in G.get_adj_nodes(current_node):
                if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                    Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                    dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                    pred[neighbour] = current_node
        return dist

