import random
from source.final_project_part1 import bellman_ford, dijkstra, total_dist
from shortest_path_approx import bellman_ford_approx, dijkstra_approx
from plotting import PlotGroup
import shortest_path_approx
import matplotlib.pyplot as plot
import source.final_project_part1 as fpp1
import os

saveFileDir = "./images/part1/"

saveFigures = True
showFigures = False

#experiment ideas

    #1. given random graphs with a constant number of nodes, 
    #   the accuracy of the total_dist as the number of k increases?

    #4. compare accuracy (based on relaxations) of dijskrta to bellman ford or whatever its called
    
    #5. see if less runtime if less relaxations?

def finish_figure(saveLocation):

    if saveFigures:
        print("Saving Figure to " + saveLocation)
        plot.savefig(saveFileDir + saveLocation, bbox_inches='tight')

    if showFigures:
        plot.show() 

    #Reset
    plot.close() 

def create_random_complete_graph(n,lower,upper):
    G = fpp1.DirectedWeightedGraph()

    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(lower,upper))
    return G

#
# ===================================================================================
#

#1. given random graphs with a constant number of nodes, 
#   the accuracy of the total_dist as the number of k increases, from EVERY node?

#On Dijkstas
def test1_d(nodeCount, lowerWeight, upperWeight, relaxationRange, token):
    return test1(nodeCount, lowerWeight, upperWeight, relaxationRange, dijkstra, dijkstra_approx, token, "Dijkstra")

def test1_bf(nodeCount, lowerWeight, upperWeight, relaxationRange, token):
    return test1(nodeCount, lowerWeight, upperWeight, relaxationRange, bellman_ford, bellman_ford_approx, token, "Bellman-Ford")

def test1(nodeCount, lowerWeight, upperWeight, relaxationRange, realfunc, approxfunc, token, alg="Unknown"):
    
    print(f'Starting Test 1{token}...')

    aplot = PlotGroup(f"{alg} Approximation Accuracy")

    realPlot = PlotGroup(f"{alg} Algorithm Total Distance")
    approxPlot = PlotGroup(f"{alg} Approximation Total Distance")

    aplot.placeLineAtFirstY0 = True

    #Generate Graph, 
    G = create_random_complete_graph(nodeCount, lowerWeight, upperWeight)

    for relaxAmount in relaxationRange:

        print(f"Starting k={relaxAmount}")
        #Define Accuracy
        actualDist = 0
        approxDist = 0
       
       #Check from Each Node
        for source in G.adj.keys():
            actualDist += total_dist(realfunc(G, source))
            approxDist += total_dist(approxfunc(G, source, relaxAmount))

        accuracy = abs(actualDist - approxDist)
        aplot.add_point(relaxAmount, accuracy);

        realPlot.add_point(relaxAmount, actualDist);
        approxPlot.add_point(relaxAmount, approxDist);

    #Setup
    plot.title(f"Difference in Total Distance of {alg} vs {alg} Approx On Graph of {nodeCount} Nodes")
    plot.xlabel(f"Number of Relaxations in the Approximation Function")
    plot.ylabel("Accuracy of Approximate Distance to Total Distance")
    
    aplot.plot()

    plot.legend()
    finish_figure(f'exp1_1{token}A.png')
  
    #
    # Second Graph
    #

    plot.title(f"Total Distances of {alg} vs {alg} Approx On Graph of {nodeCount} Nodes")
    plot.xlabel(f"Number of Relaxations in the Approximation Function")
    plot.ylabel("Accuracy of Approximate Distance to Total Distance")
    
    realPlot.plot()
    approxPlot.plot()

    plot.legend()
    finish_figure(f'exp1_1{token}B.png')


# ===================================================================================
#

#
#As relaxations increase, how does the accuracy fair from some single starting node?
def test4(nodeCount, lowerWeight, upperWeight, relaxationRange, startingNode, trials, token):

    print(f'Starting Test 4{token}...')

    dplot = PlotGroup(f"Dijkstra Approximation Accuracy")
    bfplot = PlotGroup(f"Bellmand Ford Approximation Accuracy")

    for relaxAmount in relaxationRange:

        print(f"Starting k={relaxAmount}")

        dActualDist = 0
        dApproxDist = 0
        bfActualDist = 0
        bfApproxDist = 0

        for _ in range(trials):
            
            #Generate Graph, 
            G = create_random_complete_graph(nodeCount, lowerWeight, upperWeight)

            dActualDist = total_dist(dijkstra(G, startingNode))
            dApproxDist = total_dist(dijkstra_approx(G, startingNode, relaxAmount))

            bfActualDist = total_dist(bellman_ford(G, startingNode))
            bfApproxDist = total_dist(bellman_ford_approx(G, startingNode, relaxAmount))

        dActualDist /= trials
        dApproxDist /= trials
        bfActualDist /= trials
        bfApproxDist /= trials

        #Plot
        dplot.add_point(relaxAmount, abs(dActualDist - dApproxDist));
        bfplot.add_point(relaxAmount, abs(bfActualDist - bfApproxDist));

       
    dplot.plot()
    bfplot.plot()

    #Setup
    plot.title(f"Difference of Total Distance between Approximation Algorithms on {nodeCount} Noded Graphs ({trials} Trials)")
    plot.xlabel("Number of Relaxations in the Approximation Function")
    plot.ylabel("Difference in Total Distance Algorithm vs Approximation")    
    plot.legend()

    finish_figure(f'exp1_4{token}.png')


#
# ===================================================================================
#

# What is the accuracy of dijsktra's as n nodes increase with constant k relaxations?

#NOTE: Many trials needed as graphs are random. However, we perform the same alg on the same graph for each trial,
#so the averages are okay. We average to get a general trend as items can vary.
def test5(nodeRange, upperWeight, constantRelaxations, startingNode, trials, token):

    print(f'Starting Test 5{token}...')

    approxPlots = []

    for relaxation in constantRelaxations:
        approxPlots.append(PlotGroup(f"{relaxation} Relaxations"))
    realPlot = PlotGroup(f"Dijkstra Total Distance", "#000000")

    for nodeCount in nodeRange:

        print(nodeCount)

        approxDists = []
        for relaxation in constantRelaxations:
            approxDists.append(0)

        realDist = 0

        for _ in range(trials):

            #Generate Graph, 
            G = create_random_complete_graph(nodeCount, 1, upperWeight)

            for i in range(len(constantRelaxations)):
                relax = constantRelaxations[i];
                approxDists[i] += total_dist(dijkstra_approx(G, startingNode, relax))

            realDist += total_dist(dijkstra(G, startingNode))

        # Average
        for i in range(len(constantRelaxations)):
            plotGroup = approxPlots[i]
            curDistance = approxDists[i]
            plotGroup.add_point(nodeCount, curDistance / trials)

        realPlot.add_point(nodeCount, realDist / trials)

    #Plot All
    for plott in approxPlots:
        plott.plot()
        print(plott)

    realPlot.plot() 

    #Setup
    plot.title(f"Dijkstra vs Dijkstra Approximations Total Distance vs Graph Node Count")
    plot.xlabel(f"Number of Nodes in graph G")
    plot.ylabel("Total Distance of Graph")    
    plot.legend()

    finish_figure(f'exp1_5{token}.png')

    pass

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def test6(nodeCount, upperWeights, constantRelaxations, startingNode, trials, token):

    print(f'Starting Test 5{token}...')

    approxPlots = []

    for relaxation in constantRelaxations:
        approxPlots.append(PlotGroup(f"{relaxation} Relaxations"))
    realPlot = PlotGroup(f"Dijkstra Total Distance", "#000000")

    for upperWeight in upperWeights:

        print(upperWeight)

        approxDists = []
        for relaxation in constantRelaxations:
            approxDists.append(0)

        realDist = 0

        for _ in range(trials):

            #Generate Graph, 
            G = create_random_complete_graph(nodeCount, 1, upperWeight)

            for i in range(len(constantRelaxations)):
                relax = constantRelaxations[i];
                approxDists[i] += total_dist(dijkstra_approx(G, startingNode, relax))

            realDist += total_dist(dijkstra(G, startingNode))

        # Average
        for i in range(len(constantRelaxations)):
            plotGroup = approxPlots[i]
            curDistance = approxDists[i]
            plotGroup.add_point(upperWeight, curDistance / trials)

        realPlot.add_point(upperWeight, realDist / trials)

    #Plot All
    for plott in approxPlots:
        plott.plot()
        print(plott)

    realPlot.plot() 

    #Setup
    plot.title(f"Dijkstra Approximations Total Distance on Random Graph n={nodeCount} vs Edge Weight Max Value ({trials} Trials)")
    plot.xlabel(f"Maximum Edge Weight (Edge Range [1..x])")
    plot.ylabel("Total Distance of Graph")    
    plot.legend()

    finish_figure(f'exp1_6{token}.png')

    pass

#
# ===================================================================================
#

if (__name__ == "__main__"):

    #Run Tests
    token = 0

    #
    # Test 1
    #
    # test1_d(50, 0, 100, range(1, 50 + 1), 'a')
    # test1_bf(25, 0, 100, range(1, 25 + 1), 'b')
    # test1_bf(25, -100, 100, range(1, 25 + 1), 'c')
    # test1_bf(25, -100, 100, range(1, 1000, 10), 'd')

    #
    # Test 4
    #
    # test4(25, 0, 100, range(2, 50), 0, 100, 'a')

    #
    # Test 5
    #
    test5(range(10, 600, 40), 100, [1, 2, 4, 6, 8], 0, 10, 'a')
    test5(range(2, 61), 100, [1, 2, 4, 6, 8], 0, 10, 'b')
    test5(range(1000, 1011, 2), 100, [1, 2, 4, 6, 8, 10], 0, 1, 'c')
    
    #
    #Test 6
    test6(10, range(1, 1000, 10), [1, 2, 4, 6, 8, 10], 0, 500, 'a')
    test6(50, range(1, 1000, 10), [1, 2, 4, 6, 8, 10], 0, 500, 'b')
    test6(100, range(1, 5000, 100), [1, 2, 4, 6, 8, 10], 0, 10, 'c')

    #End
    pass