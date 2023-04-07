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
    
    #5. see if less runtime if less relaxations?


#
# ===================================================================================
#

#1. given random graphs with a constant number of nodes, 
#   the accuracy of the total_dist as the number of k increases, from EVERY node?

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
    
    plot.legend()
    aplot.plot()
    plot.show()


# ===================================================================================
#

#
#As relaxations increase, how does the accuracy fair from some single starting node?
def test4(nodeCount, upperWeight, relaxationRange, startingNode):

    
    dplot = PlotGroup(f"Dijkstra Approximation Accuracy")
    bfplot = PlotGroup(f"Bellmand Ford Approximation Accuracy")

    #Generate Graph, 
    G = create_random_complete_graph(nodeCount, upperWeight)

    for relaxAmount in relaxationRange:

        print(f"Starting k={relaxAmount}")
        
        #Define Accuracy
        dActualDist = 0
        dApproxDist = 0

        bfActualDist = 0
        bfApproxDist = 0
       
       #Check from Each Node
        dActualDist += total_dist(dijkstra(G, startingNode))
        dApproxDist += total_dist(dijkstra_approx(G, startingNode, relaxAmount))

        bfActualDist += total_dist(bellman_ford(G, startingNode))
        bfApproxDist += total_dist(bellman_ford_approx(G, startingNode, relaxAmount))

        #Plot
        dplot.add_point(relaxAmount, dActualDist / dApproxDist);
        bfplot.add_point(relaxAmount, bfActualDist / bfApproxDist);

       
    dplot.plot()
    bfplot.plot()

    #Setup
    plot.title(f"Comparing Accuracies of total distances between Approximation Algorithms with x allowed relaxations from Starting Node {startingNode}")
    plot.xlabel(f"Number of Relaxations in the Approximation Function")
    plot.ylabel("Accuracy of Approximate Distance to Total Distance")    
    plot.legend()
    plot.show()


#
# ===================================================================================
#

# What is the accuracy of dijsktra's as n nodes increase with constant k relaxations?

#NOTE: Many trials needed as graphs are random. However, we perform the same alg on the same graph for each trial,
#so the averages are okay. We average to get a general trend as items can vary.
def test5(nodeRange, upperWeight, constantRelaxations, startingNode, trials):

    approxPlots = []

    for relaxation in constantRelaxations:
        approxPlots.append(PlotGroup(f"Dijkstra Approximation {constantRelaxations} Relaxations Total Distance"))
    realPlot = PlotGroup(f"Dijkstra Total Distance")

    for nodeCount in nodeRange:

        print(nodeCount)

        approxDists = []
        for relaxation in constantRelaxations:
            approxDists.append(0)

        realDist = 0

        for _ in range(trials):

            #Generate Graph, 
            G = create_random_complete_graph(nodeCount, upperWeight)

            for i in range(len(constantRelaxations)):
                approxDists[i] += total_dist(dijkstra_approx(G, startingNode, constantRelaxations[i]))

            realDist += total_dist(dijkstra(G, startingNode))

        # Average
        for i in range(len(constantRelaxations)):
            approxPlots[i].add_point(nodeCount, approxDists[i] / trials)

        realPlot.add_point(nodeCount, realDist / trials)

    #Plot All
    for i in range(len(constantRelaxations)):
        approxPlots[i].plot()
    realPlot.plot()

    #Setup
    plot.title(f"Average Total Distance of {trials} Trials of Dijkstra vs Dijkstra Approximation with constant {constantRelaxations} Relaxations")
    plot.xlabel(f"Number of Nodes in graph G")
    plot.ylabel("Total Distance of graph")    
    plot.legend()
    plot.show()

    pass

#
# ===================================================================================
#

if (__name__ == "__main__"):

    #Run Tests

    #
    # Test 1
    #
    
    #test1_d(50, 100, range(50 + 1))
    # test1_bf(25, 100, range(1, 25 + 1))

    #
    # Test 2
    #


    #
    # Test 3
    #


    #
    # Test 4
    #

    # test4(50, 100, range(20 + 1), 0)
    # test4(50, 100, range(20 + 1), 25)

    #
    # Test 5
    #
    test5(range(10, 100, 10), 100, [1, 10, 20, 50, 100], 0, 1000)


    #End
    pass