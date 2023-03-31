from source.final_project_part1 import bellman_ford, dijkstra
from source.final_project_part1 import create_random_complete_graph, total_dist
from shortest_path_approx import bellman_ford_approx, dijkstra_approx
from plotting import PlotGroup
import shortest_path_approx
import matplotlib.pyplot as plot
import source.final_project_part1

#experiment ideas
    #1. given random graphs with a constant number of nodes, 
    #   the accuracy of the total_dist as the number of k increases?

    #4. compare accuracy (based on relaxations) of dijskrta to bellman ford or whatever its called
    
    #5. see if less runtime if less relaxations??

#
# ===================================================================================
#

#1. given random graphs with a constant number of nodes, 
#   the accuracy of the total_dist as the number of k increases?

#On Dijkstas
def test1_d(nodeCount, upperWeight, relaxationRange):
    return test1(nodeCount, upperWeight, relaxationRange, dijkstra, dijkstra_approx, "Dijkstra")

def test1_bf(nodeCount, upperWeight, relaxationRange):
    return test1(nodeCount, upperWeight, relaxationRange, bellman_ford, bellman_ford_approx, "Bellman Ford")

def test1(nodeCount, upperWeight, relaxationRange, realfunc, approxfunc, alg="Unknown"):
    
    aplot = PlotGroup(f"{alg} Approximation Accuracy")
    #Generate Graph, 
    G = create_random_complete_graph(nodeCount, upperWeight)

    for relaxAmount in relaxationRange:

        print(f"Starting k={relaxAmount}")
        #Define Accuracy
        actualDist = 0
        approxDist = 0
       
       #Check from Each Node
        for source in G.adj.keys():
            actualDist += total_dist(realfunc(G, source))
            approxDist += total_dist(approxfunc(G, source, relaxAmount))

        accuracy = actualDist / approxDist 
        aplot.add_point(relaxAmount, accuracy);

    #Setup
    plot.title(f"Accuracy of the Total Distance of {alg} Real vs {alg} Approx with x relaxations")
    plot.xlabel(f"Number of Relaxations in the Approximation Function")
    plot.ylabel("Accuracy of Approximate Distance to Total Distance")
    
    aplot.plot()
    plot.show()

    # Reals






#
# ===================================================================================
#

def test2():
    pass


#
# ===================================================================================
#

def test3():
    pass


#
# ===================================================================================
#

def test4():
    pass


#
# ===================================================================================
#

def test5():
    pass

#
# ===================================================================================
#

if (__name__ == "__main__"):

    #Run Tests

    #
    # Test 1
    #
    test1_d(50, 100, range(50 + 1))

    #
    # Test 2
    #


    #
    # Test 3
    #


    #
    # Test 4
    #


    #
    # Test 5
    #

    #End
    pass