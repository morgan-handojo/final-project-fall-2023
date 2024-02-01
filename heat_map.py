"""
Morgan Handojo
Kara Fowler
"""

import os
import sys
import numpy as np
from project_queue import Queue
from heat_node import HeatNode
from color_for_temp import Color


os.system("")
# reset the terminal color
RESET_CHAR = "\u001b[0m"
# color codes for the terminal
COLOR_DICT = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m"
}
# block
BLOCK_CHAR = "\u2588"

def colored(text, color):
    color = color.strip().lower()
    return COLOR_DICT[color] + text

# prints the actual bloc char for our ouput lol
def print_block(color):
    print(colored(BLOCK_CHAR, color)*2, end='')

# this makes the actual graph
class ImageGraph:
    def __init__(self, image_size, edge_temps):
        # temp matrix stores the calculated temperatures of each node
        # edge_temps is the temps around each corner [left, top, right, bottom]
        self.nodes = []
        self.image_size = image_size
        self.temp_matrix = []
        self.edge_temps = edge_temps

    # prints the image formed by the nodes on the command line
    def print_image(self):
        image = [["black" for i in range(self.image_size)] for j in range(self.image_size)]

        # fill image array
        for node in self.nodes:
            image[node.y][node.x] = node.color

        for line in image:
            for pixel in line:
                print_block(pixel)
            print()
        # print new line/reset color
        print(RESET_CHAR)


    # creates a matrix of temperature that corresponds to the index of the node graph thing
    def temperature_matrix(self, edge_temps):
        matrix_A = [[0 for col in range(len(self.nodes))] for row in range(len(self.nodes))]
        matrix_b = [[0 for col in range(1)] for row in range(len(self.nodes))]

        row = 0
        for thing in self.nodes:
            cur_edges = thing.edges
            cur_label = thing.index
            cur_side = 0
            # sets top side
            if cur_label < self.image_size:
                cur_side += int(edge_temps[0])
            #sets bottom side
            elif row == self.image_size-1:
                cur_side += int(edge_temps[2])
            # sets right side
            elif cur_label%(self.image_size) == (self.image_size - 1):
                cur_side += int(edge_temps[3])
            # sets left side
            elif (cur_label % (self.image_size)) == 0:
                cur_side += int(edge_temps[1])

            matrix_A[row][cur_label] = -4
            for edge in cur_edges:
                matrix_A[row][edge] = 1
            # if corner node and for B matrix
            if len(cur_edges) == 2:
                matrix_b[row] = [-cur_side]
            # if side node
            if len(cur_edges) == 3:
                matrix_b[row] = [-cur_side]
            #if interior node
            if len(cur_edges) == 4:
                matrix_b[row] = [0]
            row += 1

        A = np.array(matrix_A)
        B = np.array(matrix_b)
        temps = np.linalg.lstsq(A,B,rcond=None)[0]

        self.temp_matrix = temps



    #   start_index is the index of the currently visited node
    def bfs(self, start_index):
        my_queue = Queue()
        my_list = []
        my_queue.enqueue(start_index)
        my_list.append(start_index)
        #creates color dictionary
        color_class_instance = Color(self.edge_temps)
        color_class_instance.color_for_temp()
        # actually makes the temp matrix
        self.temperature_matrix(self.edge_temps)
        #print(self.temp_matrix)


        while not my_queue.is_empty():
            current_node = my_queue.dequeue()
            my_list.pop(0)

            # needs to grab specific color based on temperature that we have calculated
            current_node_temp = self.temp_matrix[current_node][0]

            # specific color based on the node from previously created color temp matrix
            color_maker = Color(self.edge_temps)
            new_color = color_maker.get_color(current_node_temp)

            self.nodes[current_node].set_color(new_color)

            next_nodes = self.nodes[current_node].edges
            for node in next_nodes:
                #if the node is black (unvisited)
                if self.nodes[node].color == "black":
                    if node not in my_list:
                        my_queue.enqueue(node)
                        my_list.append(node)
            # uncomment below to see graph being built
            #self.print_image()
        print("Temps:\n    Left:", self.edge_temps[0], "\n    Top:", self.edge_temps[1], "\n    Right:", self.edge_temps[2], "\n    Bottom:", self.edge_temps[3])
        self.print_image()


def create_graph(data):
    data_list = data.split("\n")

    # get size of image, number of nodes, and the edge temp
    image_size = int(data_list[0])
    node_count = int(data_list[1])
    edge_temps = data_list[len(data_list) - 1].split(",")

    graph = ImageGraph(image_size, edge_temps)
    index = 2

    # create nodes
    for i in range(node_count):
        node_info = data_list[index].split(",")
        new_node = HeatNode(len(graph.nodes), int(node_info[0]), int(node_info[1]), "black")
        graph.nodes.append(new_node)
        index += 1

    # read edge count
    edge_count = int(data_list[index])
    index += 1

    # create edges between nodes
    for i in range(edge_count):
        # edge info has the format "fromIndex,toIndex"
        edge_info = data_list[index].split(",")
        # connect node 1 to node 2 and the other way around
        graph.nodes[int(edge_info[0])].add_edge(int(edge_info[1]))
        graph.nodes[int(edge_info[1])].add_edge(int(edge_info[0]))
        index += 1

    # read search info
    search_info = data_list[index].split(",")
    search_start = int(search_info[0])

    return graph, search_start



def main():
    # read input
    data = sys.stdin.read()

    graph, search_start = create_graph(data)


    # run bfs
    graph.bfs(search_start)


if __name__ == "__main__":
    main()