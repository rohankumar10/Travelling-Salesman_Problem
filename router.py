from itertools import *
import timeit
import copy


class BranchNBound:
    def __init__(self, matrix):
        self.matrix = matrix

    def GeneratePaths(self, matrix_called):
        # Extracting the nodes of the TSP
        lstNodes = [node for node in range(len(matrix_called))]
        # Remove the last city to generate non cyclic permutations
        last_node = lstNodes.pop()
        # Enumerating all the paths from the nodes
        lstPermutations = list(permutations(lstNodes))
        # Constructing a tree
        lstTree = list(map(list, lstPermutations))

        # Closing the paths / Constructing full cycles
        for path in lstTree:
            path.append(last_node)
            path.append(path[0])
        return lstNodes, lstTree

    def branch_bound(self):
        start = timeit.default_timer()
        # Generate the TSP nodes and all the possible paths
        lstNodes, lstTree = self.GeneratePaths(self.matrix)

        # Calculating the cost of each cycle
        lstCostList = []
        # Initialize the current best/optimal cost to infinity
        numCurrentBestCost = float("inf")
        for cycle in lstTree:
            # Initialize cost for each cycle
            numCostPerCycle = 0
            # Convert each 2 nodes in a cycle to an index in the input array
            for index in range(0, (len(lstNodes) - 1)):
                # CostPerCycle is calculated from the input Matrix between
                #   each 2 nodes in a cycle
                numCostPerCycle = numCostPerCycle + self.matrix[cycle[index]][cycle[index + 1]]
                # Check the current accumlated cost against the Current Best Cost
                if (numCostPerCycle >= numCurrentBestCost):
                    numCostPerCycle = float("inf")
                    break

            # Add the first cycle cost as the best one
            if (numCurrentBestCost == float("inf")):
                numCurrentBestCost = numCostPerCycle
            # if a better cost is found, update the numCurrentBestCost variable
            elif (numCostPerCycle < numCurrentBestCost):
                numCurrentBestCost = numCostPerCycle
            # Add the current cycle cost to the cost list
            lstCostList.append(numCostPerCycle)

        # Calculating the least cost cycle
        numLeastCost = min(lstCostList)
        numLeastCostIndex = lstCostList.index(numLeastCost)
        stop = timeit.default_timer()
        time_finish = stop - start
        BnB_output = ["Branch and Bound", numLeastCost, lstTree[numLeastCostIndex], time_finish]
        print(BnB_output)
        return BnB_output


class Greedy:
    def __init__(self, matrix):
        self.matrix = matrix

    def greedy(self, matrix_called, start_city=0):


        # Path of the tour
        path = [start_city]
        # Cost of the tour
        cost = 0
        # Assume the first city as starting point, create a temporary value
        temp = start_city
        # Hold the position in the list
        position = start_city
        # The number of the unvisited cities
        flag = len(matrix_called) - 1
        # Current cost
        current_cost = 0
        while flag > 0:
            # Find the nearest city
            for x in range(0, len(matrix_called)):
                # x not in path, mean we don't care about the cities that we visited
                if (matrix_called[temp][x] != 0) and (x not in path):
                    if current_cost == 0:
                        current_cost = matrix_called[temp][x]
                        position = x
                    if current_cost > matrix_called[temp][x]:
                        current_cost = matrix_called[temp][x]
                        position = x
            cost += int(current_cost)
            # Reset current cost for next calculating
            current_cost = 0
            temp = position
            path.append(position)
            if flag == 1:
                # Add the connected path from last city to the start city
                current_cost = matrix_called[position][start_city]
                cost += current_cost
                path.append(start_city)
            flag -= 1
        algorithm = "Greedy"
        result = [algorithm, cost, path]
        # print "The cost of the tour is:"+str(result[1])
        # print "The path of the tour is:"+str(result[2])
        # print "The time to finish is:"+str(result[3])+" in second"
        return result

    def better_greedy(self):
        start = timeit.default_timer()
        # print "greedy algorithm is running. Please wait!"
        result = self.greedy(self.matrix, 0)
        result_temp = []
        i = 0
        while i < len(self.matrix):
            result_temp = self.greedy(self.matrix, i)
            if result[1] > result_temp[1]:
                result = result_temp
            i += 1
        stop = timeit.default_timer()
        # print "The best result:"
        print("The cost of the tour is:" + str(result[1]))
        print("The path of the tour is:" + str(result[2]))
        stop = timeit.default_timer()
        time_finish = stop - start
        print(result)
        print("The time to finish is:", time_finish)
        return result


class OptimumGreedy:
    def __init__(self, matrix, data):
        self.matrix = matrix
        self.data = data
        self.all_sets = []
        self.g = {}
        self.p = []

    def get_minimum(self, k, a):
        if (k, a) in self.g:
            # Already calculated Set g[%d, (%s)]=%d' % (k, str(a), g[k, a]))
            return self.g[k, a]

        values = []
        all_min = []
        for j in a:
            set_a = copy.deepcopy(list(a))
            set_a.remove(j)
            all_min.append([j, tuple(set_a)])
            result = self.get_minimum(j, tuple(set_a))
            values.append(matrix[k - 1][j - 1] + result)

        # get minimun value from set as optimal solution for
        self.g[k, a] = min(values)
        self.p.append(((k, a), all_min[values.index(self.g[k, a])]))

        return self.g[k, a]

    def optimum_greedy(self):
        start = timeit.default_timer()
        n = len(self.data)
        for x in range(1, n):
            self.g[x + 1, ()] = self.matrix[x][0]

        self.get_minimum(1, (2, 3, 4, 5))

        print('\n\nSolution to TSP: {1, ', end='')
        solution = self.p.pop()
        print(solution[1][0], end=', ')
        for x in range(n - 2):
            for new_solution in self.p:
                if tuple(solution[1]) == new_solution[0]:
                    solution = new_solution
                    print(solution[1][0], end=', ')
                    break
        print('1}')

        stop = timeit.default_timer()
        time_finish = stop - start
        print("Time taken:-", time_finish)
        return


class BruteForce:
    def __init__(self, matrix):
        self.matrix = matrix

    def GeneratePaths(self, matrix_called):
        # Extracting the nodes of the TSP
        lstNodes = [node for node in range(len(matrix_called))]
        # Remove the last city to generate non cyclic permutations
        last_node = lstNodes.pop()
        # Enumerating all the paths from the nodes
        lstPermutations = list(permutations(lstNodes))
        # Constructing a tree
        lstTree = list(map(list, lstPermutations))

        # Closing the paths / Constructing full cycles
        for path in lstTree:
            path.append(last_node)
            path.append(path[0])
        return lstNodes, lstTree

    def bruteforce(self):
        start = timeit.default_timer()
        # Generate all the possible paths
        lstNodes, lstTree = self.GeneratePaths(self.matrix)

        # Calculating the cost of each cycle
        lstCostList = []
        for cycle in lstTree:
            # Initialize cost for each cycle
            numCostPerCycle = 0
            # Convert each 2 nodes in a cycle to an index in the input array
            for index in range(0, (len(lstNodes) - 1)):
                # CostPerCycle is calculated from the input Matrix between
                #   each 2 nodes in a cycle
                numCostPerCycle = numCostPerCycle + self.matrix[cycle[index]][cycle[index + 1]]
            lstCostList.append(numCostPerCycle)

        # Calculating the least cost cycle
        numLeastCost = min(lstCostList)
        numLeastCostIndex = lstCostList.index(numLeastCost)
        stop = timeit.default_timer()
        time_finish = stop - start
        BF_output = ["Brute Force", numLeastCost, lstTree[numLeastCostIndex], time_finish]
        print(BF_output)


matrix = [
    [0, 20, 30, 10, 11],
    [15, 0, 16, 4, 2],
    [3, 5, 0, 2, 4],
    [19, 6, 18, 0, 3],
    [16, 4, 7, 16, 0]
]
data = [1, 2, 3, 4, 5]

ans = True
while ans:
    print("""
    1.Branch N Bound
    2.Greedy
    3.Optimum Greedy
    4.Brute Force
    5.Exit/Quit
    """)
    ans = input("What would you like to do? ")
    if ans == "1":
        algo1 = BranchNBound(matrix)
        algo1.branch_bound()
    elif ans == "2":
        algo2 = Greedy(matrix)
        algo2.better_greedy()
    elif ans == "3":
        algo3 = OptimumGreedy(matrix, data)
        algo3.optimum_greedy()
    elif ans == "4":
        algo4 = BruteForce(matrix)
        algo4.bruteforce()
    elif ans == "5":
        print("\n Goodbye")
        exit()
    elif ans != "":
        print("\n Not Valid Choice Try again")

