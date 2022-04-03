""" Checking the acceptance of a word by a Mealy machine """
# We want to memorize the graph in a dictionary structure, where the pair key:value has the following interpretation
#               node1: [(next_node1, input1, output1), ...]
#   in other words, if we know that from the node I we can go to node J, processing 'a' from the word and printing 'b',
# the pair in the dictionary will take the form: I: [(J, a, b)];
#   then, if from the same node I we can go to node K, processing 'c' from the word and printing 'd', the dictionary
#  will be updated as follows: I: [(J, a, b), (K, c, d)]

graph = {}


def add_edge(node_start, node_end, cost, output):
    global graph
    global total_nodes
    if node_start not in graph.keys():
        graph[node_start] = []
    if node_end not in graph.keys():
        graph[node_end] = []
    graph[node_start].append((node_end, cost, output))


def print_graph():
    global graph
    for node in graph.keys():
        for edge in graph[node]:
            print(node, "->", edge[0], " process:", edge[1], " print:", edge[2])


def search(start_node, word):
    global graph
    i = 0
    n = len(word)
    current_node = start_node
    path = []
    while i < n:
        ok = 0
        for edge in graph[current_node]:
            if edge[1] == word[i]:
                path += [(current_node, edge)]
                current_node = edge[0]
                ok = 1
                break
        if ok == 0:
            return -1
        i = i + 1
    return path


# reading all the information from the input file
# the input file has the following structure
# number_of_nodes number_of_edges
# list of edges(each on a different line) under the form: start_node end_node letter_to_process output
# start_state
# number_of_final_states list_of_final_states (delimited using space)
# number_of_words to be checked
# the rest or the lines will contain strings with the words to be checked by the machine
f = open("graph.txt", "r")
line = f.readline().split()
total_nodes, total_edges = int(line[0]), int(line[1])
edges_list = []
i = 0
while i < total_edges:
    edge = f.readline().split()
    edges_list.append(edge)
    i = i + 1
start_state = f.readline().split()[0]
line = f.readline().split()
final_state_total = int(line[0])
final_states = []
i = 0
while i < final_state_total:
    final_states.append(line[i + 1])
    i = i + 1
total_words_to_check = int(f.readline())
to_check = []
i = 0
while i < total_words_to_check:
    to_check.append(f.readline().strip())
    i = i + 1
# creating the graph
for pair in edges_list:
    add_edge(*pair)
# print_graph()

# for each word that we need to check, we will start at the start_state of the machine and check if we can move further
# with the next letter that needs to be processed; if at any point there is no way to continue, we can surely affirm
# that the word can't be processed; also, if we finish processing the word and we are not in a final state, the word
# will once again not be accepted.
# during the search, we will save information about the path we have taken up to the current iteration (as well as what
# the processed part of the word will output) as a list of tuples with two components: the current node and the
# information found in the graph dictionary we have previously created for the following node that is reached by
# processing the next letter of the word.

for i in range(0, total_words_to_check):
    print("Cuvant " + str(i + 1) + ":", end=" ")
    if search(start_state, to_check[i]) == -1:
        print("NU")
    else:
        path = search(start_state, to_check[i])
        if path[len(path) - 1][1][0] not in final_states:
            print("NU")
        else:
            print("DA")
            print("     Output:", end=" ")
            for x in path:
                print(x[1][2], end="")
            print()
            print("     Traseu:", end=" ")
            print(start_state, end=" ")
            for x in path:
                print(x[1][0], end=" ")
            print()

"""
First input file:
4 8
0 1 a 0
1 1 b 1
1 2 c 2
1 3 a 1
2 2 c 2
2 3 a 1
3 3 a 0
3 3 c 3
0
1 3
4
cc
abbacccc
ac
accccaa

Second input file:
3 7
q0 q0 1 b
q0 q1 0 b
q1 q0 0 b
q1 q1 0 b
q1 q2 1 a
q2 q1 0 b
q2 q0 1 b
q0
2 q2 q0
3
10111001
001010110100
010010100110
"""
