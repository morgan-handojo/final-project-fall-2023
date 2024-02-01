# divides up the temperatures into diff colors
# second function will RETURN THE COLOR OF THE BLOCK THAT WE WILL BE COLORING IN BFS
class Color:
#input edge_temps is a list
    def __init__(self, edge_temps):
        self.color_dict = dict()
        int_edges = []
        for edge in edge_temps:
            int_edges.append(int(edge))
        self.edge_temps = int_edges

    def color_for_temp(self):
        colors = ["white", "red", "yellow", "green", "cyan", "blue", "magenta"]
        highest = int(max(self.edge_temps))
        lowest = int(min(self.edge_temps))

        the_range = highest - lowest
        increment = the_range / 7
        count = 0
        # hottest to coolest color
        for color in colors:
            if color == "magenta":
                self.color_dict[color] = (int(lowest + increment), lowest - 1)
            else:
                self.color_dict[color] = (int(highest - (increment * count)), int(highest - (increment * (count + 1))))
                count += 1
        return self.color_dict
    # temp ranges should be read as greater than the lower bound, and less than or equal to the high bound

    def get_color(self, temp):
        colors = ["white", "red", "yellow", "green", "cyan", "blue", "magenta"]
        self.color_for_temp()
        for color in colors:
            if temp <= self.color_dict[color][0] and temp > self.color_dict[color][1]:
                return color


