import csv
from collections import defaultdict
import WeightedGraph
import geopy.distance
import random
from plotting import PlotGroup
import a_star
import Dijsktra
import timeit
import matplotlib.pyplot as plot


TRIALS = 15
combos = 20


def parse_connections_csv(path):
    with open(path, 'r') as file:
        d = WeightedGraph.WeightedGraph()
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row['station1'] not in d.adj:
                d.add_node(row['station1'])
            if row['station2'] not in d.adj:
                d.add_node(row['station2'])
            d.add_edge(row['station1'], row['station2'],
                       int(row['time']), row['line'])
        return d


def parse_stations_csv(path):
    with open(path, 'r') as file:
        csv_file = csv.DictReader(file)
        d = defaultdict(dict)
        for row in csv_file:
            d[row['id']] = {'latitude': row['latitude'], 'longitude': row['longitude'], 'name': row['name'],
                            'display_name': row['display_name'], 'zone': row['zone'], 'total_lines': row['total_lines'], 'rail': row['rail']}
        return d


def distance(coords1, coords2):
    return geopy.distance.distance(coords1, coords2).km


def general_experiments():
    # Here we will conduct 100 trials to test where the A* algorithm is faster than Dijkstra's algorithm
    # We will use the same graph for each trial, and test the time taken for each algorithm to find the shortest path between all pairs of stations

    # Load the data
    connections = parse_connections_csv('source/london_connections.csv')
    stations = parse_stations_csv('source/london_stations.csv')

    djikstra_performace = PlotGroup('Dijkstra', '#ff4d4d')
    a_star_performance = PlotGroup('A*', '#359cff')

    # Choose two random stations
    for i in range(TRIALS):
        print(f'Running Trial {i}')
        timea = 0
        timed = 0
        seen = set()

        # Iterate through all pairs of stations
        for source in stations:
            for dest in stations:
                # If the source and destination are the same, skip
                if source == dest or (source, dest) in seen or (dest, source) in seen:
                    continue

                seen.add((source, dest))
                seen.add((dest, source))

                # Generate the heuristic dictionary
                h = {}

                for station in stations:
                    h[station] = distance((stations[station]['latitude'], stations[station]['longitude']),
                                          (stations[dest]['latitude'], stations[dest]['longitude']))

                # Run A*
                try:
                    print(f'Running A* from {source} to {dest}')
                    start = timeit.default_timer()
                    a_star.a_star(connections, source, dest, h)
                    stop = timeit.default_timer()
                    timea += stop - start
                except:
                    print('A* failed')

                # Run Dijkstra's
                print(f'Running Dijkstra from {source} to {dest}')
                start = timeit.default_timer()
                Dijsktra.dijkstra(connections, source, dest)
                stop = timeit.default_timer()
                timed += stop - start

        # Add the average time taken for each trial to the plot
        djikstra_performace.add_point(
            i, timed / (len(stations) * (len(stations) - 1)))
        a_star_performance.add_point(
            i, timea / (len(stations) * (len(stations) - 1)))

    # Plot the results
    djikstra_performace.plot()
    a_star_performance.plot()
    plot.title(
        'Average Time Taken for A* and Dijkstra\'s Algorithm to Find the Shortest Path Between All Pairs of Stations')
    plot.xlabel('Trial Number')
    plot.ylabel('Average Time Taken (s)')

    plot.legend()
    plot.show()


def same_zone_experiments():

    # Load the data
    connections = parse_connections_csv('source/london_connections.csv')
    stations = parse_stations_csv('source/london_stations.csv')

    djikstra_performace = PlotGroup('Dijkstra', '#ff4d4d')
    a_star_performance = PlotGroup('A*', '#359cff')

    # Choose two random stations
    for i in range(TRIALS):
        print(f'Running Trial {i}')
        timea = 0
        timed = 0
        seen = set()

        stimes = 0
        dtimes = 0

        # Iterate through all pairs of stations
        keys = list(stations.keys())
        random.shuffle(keys)
        for source in keys:
            if stimes == combos:
                break
            for dest in keys:
                # If the source and destination are the same, skip
                if source == dest or stations[source]['zone'] != stations[dest]['zone'] or (source, dest) in seen or (dest, source) in seen:
                    continue

                dtimes += 1
                print(f'stime is {stimes}, dtimes is {dtimes}')

                seen.add((source, dest))
                seen.add((dest, source))
                # Generate the heuristic dictionary
                h = {}

                for station in stations:
                    h[station] = distance((stations[station]['latitude'], stations[station]['longitude']),
                                          (stations[dest]['latitude'], stations[dest]['longitude']))

                # Run A*
                try:
                    print(f'Running A* from {source} to {dest}')
                    start = timeit.default_timer()
                    a_star.a_star(connections, source, dest, h)
                    stop = timeit.default_timer()
                    timea += stop - start
                except:
                    print('A* failed')

                # Run Dijkstra's
                print(f'Running Dijkstra from {source} to {dest}')
                start = timeit.default_timer()
                Dijsktra.dijkstra(connections, source, dest)
                stop = timeit.default_timer()
                timed += stop - start

                if dtimes == combos:
                    dtimes = 0
                    stimes += 1
                    break

        # Add the average time taken for each trial to the plot
        djikstra_performace.add_point(
            i, timed / (combos * combos))
        a_star_performance.add_point(
            i, timea / (combos * combos))

    # Plot the results
    djikstra_performace.plot()
    a_star_performance.plot()
    plot.title(
        'Average Time Taken for A* and Dijkstra\'s Algorithm to Find the Shortest Path Between All Pairs of Stations in the Same Zone')
    plot.xlabel('Trial Number')
    plot.ylabel('Average Time Taken (s)')

    plot.legend()
    plot.show()


same_zone_experiments()
