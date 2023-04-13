import min_heap
from SPAlgorithm import SPAlgorithm


class A_star(SPAlgorithm):
    
    def calc_sp(self, graph, source, dest):
        return self.calc_sp_aux(graph, source, dest, graph.get_heuristic())
        
    def calc_sp_aux(self,G, source, dest, h):
        pred = {} #Predecessor dictionary
        dist = {} #Distance dictionary
        Q = min_heap.MinHeap([])
        nodes = list(G.adj.keys())

        #Initialize priority queue/heap and distances
        for node in nodes:
            Q.insert(min_heap.Element(node, float("inf")))
            dist[node] = float("inf")
        Q.decrease_key(source, 0)

        #Meat of the algorithm
        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value
            if current_node == dest:
                break
            if current_element.key != float("inf"):
                dist[current_node] = current_element.key - h[current_node]
            else: 
                dist[current_node] = current_element.key
            for neighbour in G.adj[current_node]:
                if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                    Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + h[neighbour])
                    dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                    pred[neighbour] = current_node
        
        path = [dest]
        while path[-1] != source:
            path.append(pred[path[-1]])
        path.reverse()

        return (pred, path)

