import timeit
from matplotlib import pyplot as plt
from plotting import PlotGroup # You have to open the code file in VSCode, not our repo
import source.final_project_part1 as fp1
import random


saveFigures = True
saveFileDir = "./images/part1/"

def finish_figure(saveLocation):

    if saveFigures:
        print("Saving Figure to " + saveLocation)
        plt.savefig(saveFileDir + saveLocation, bbox_inches='tight')

    plt.show()

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

def determiningTimeComplexity(k = 5):

    # Plots
    emptyPlot = PlotGroup("Graph X Nodes, 0 Edges")
    densePlot = PlotGroup("Graph X Nodes, Total Edges")
    xtwo = PlotGroup("x^2")
    xthree = PlotGroup("x^3")

    for n in range(0, 501, 50):

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
            for i in range(n):
                for j in range(n):
                    w = random.randrange(-n*10, n*10)
                    G.add_edge(i, j, w)

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
        xtwo.add_point(n, n**2)

        print(f'Plotted n={n}')

    #
    # Graph
    plt.title("Time to Compute Mystery Function vs Weighted Edge Node Count (Log Graph)")
    emptyPlot.plotlog()
    densePlot.plotlog()
    xtwo.plotlog()
    xthree.plotlog()

    plt.xlabel("Size of Graph")
    plt.xlabel("Time To Perform Mystery Function")
    plt.legend()
    
    finish_figure("mysteryLog.png")

    #
    # Graph Again
    #

    plt.title("Time to Compute Mystery Function vs Weighted Edge Node Count")
    emptyPlot.plot()
    densePlot.plot()

    plt.xlabel("Size of Graph")
    plt.xlabel("Time To Perform Mystery Function")
    plt.legend()

    finish_figure("mysteryReal.png")

#
#
#
if (__name__ == '__main__'):

    #testing()
    determiningTimeComplexity()