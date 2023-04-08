
class ShortPathFinder:
    def __init__(self):
        self.graph = None
        self.alg = None
    
    def set_graph(self, graph):
        self.graph = graph
    
    def set_algorithm(self, alg):
        self.alg = alg
    
    def calc_short_path(self, source, dest):
        return self.alg.calc_sp(self.graph, source, dest)
