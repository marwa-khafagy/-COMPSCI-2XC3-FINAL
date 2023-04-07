import timeit
from matplotlib import pyplot as plt
from plotting import PlotGroup # You have to open the code file in VSCode, not our repo
import source.final_project_part1 as fp1

#
# Generate Small Graphs
#

def testing():

    # Small 
    G = fp1.DirectedWeightedGraph()
    G.add_node(0)
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_edge(0, 1, 5)
    G.add_edge(1, 4, 10)
    G.add_edge(3, 2, 15)
    G.add_edge(1, 3, 20)
    result = fp1.mystery(G);
    print(result)

    # Small Negatie
    G = fp1.DirectedWeightedGraph()
    G.add_node(0)
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_edge(0, 1, -5)
    G.add_edge(1, 4, 10)
    G.add_edge(3, 2, -15)
    G.add_edge(1, 3, 20)
    result = fp1.mystery(G);
    print(result)

#
#
#

def determiningTimeComplexity(k = 10):

    # Plots
    emptyPlot = PlotGroup("Graph X Nodes, 0 Edges")
    densePlot = PlotGroup("Graph X Nodes, Total Edges")
    xthree = PlotGroup("x^3")

    logScale = [0, 1, 2, 4, 8, 16, 32, 64, 96, 128, 192, 256, 320, 512]
    for n in logScale:

        #Times
        emptyTime = 0
        denseTime = 0

        for _ in range(k):

            #New Graph, Empty other than nodes
            G = fp1.DirectedWeightedGraph()
            for i in range(n):
                G.add_node(i)

            #Run Mystery
            start = timeit.default_timer()
            fp1.mystery(G)
            end = timeit.default_timer()

            emptyTime += end - start

            #
            # Fully Populate Graph
            #
            G = G

            # Retime Mystery on Full
            start = timeit.default_timer()
            fp1.mystery(G)
            end = timeit.default_timer()

            # Store
            denseTime += end - start
        
        #
        # Add Point
        emptyPlot.add_point(n, emptyTime / k)
        densePlot.add_point(n, denseTime / k)
        xthree.add_point(n, n**3)

        print(f'Plotted n={n}')

    #
    # Graph

    plt.title("Time to Compute Mystery Function vs Weighted Edge Node Count (Log Graph)")
    emptyPlot.plotlog()
    densePlot.plotlog()
    xthree.plotlog()
    
    plt.legend()
    plt.show()

    plt.title("Time to Compute Mystery Function vs Weighted Edge Node Count")
    emptyPlot.plot()
    densePlot.plot()
    xthree.plot()

    plt.legend()
    plt.show()

determiningTimeComplexity()