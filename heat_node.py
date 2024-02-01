class HeatNode:
    def __init__(self, index, x, y, color, temp = None):
        self.index = index
        self.color = color
        self.x = x
        self.y = y
        self.edges = []
        self.temp = temp

    def add_edge(self, node_index):
        """adds an edge"""
        self.edges.append(node_index)


    # sets the color of the calculated color we want it to be based on temp
    def set_color(self, color):
        """visits the node and makes sure to set it a certain color based on the given color"""
        self.color = color
