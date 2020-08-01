from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Graph:
    def __init__(self):
        self.vertices = {}

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        visited = set()

        stack = Stack()
        stack.push([starting_vertex])

        while stack.size() > 0:
            current_node = stack.pop()
            room = current_node[-1]
            if room not in visited:
                self.vertices[room.id] = {}
                for possible_direction in room.get_exits():
                    self.vertices[room.id][
                        room.get_room_in_direction(possible_direction).id
                    ] = possible_direction
                visited.add(room)
                exits = room.get_exits()

                while len(exits) > 0:
                    direction = exits[0]
                    neighbor_path = list(current_node)
                    neighbor_path.append(room.get_room_in_direction(direction))
                    stack.push(neighbor_path)
                    exits.remove(direction)
        return self.vertices

    def bfs(self, starting_vertex, destination_vertex):
        """
            Return a list containing the shortest path from
            starting_vertex to destination_vertex in
            breath-first order.
            """

        q = Queue()

        q.enqueue([starting_vertex])

        visited = set()

        while q.size() > 0:

            current_path = q.dequeue()

            last_vertex = current_path[-1]

            if last_vertex not in visited:
                if last_vertex == destination_vertex:
                    return current_path

                visited.add(last_vertex)

                for room_id in self.vertices[last_vertex].keys():
                    neighbor_path = list(current_path)
                    neighbor_path.append(room_id)
                    q.enqueue(neighbor_path)


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

world.print_rooms()

player = Player(world.starting_room)

graph = Graph()

rooms_obj_dft = graph.dft(player.current_room)

rooms_list_dft = [room_id for room_id in rooms_obj_dft.keys()]

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

while len(rooms_list_dft) > 1:

    current_room = rooms_list_dft[0]
    next_room = rooms_list_dft[1]
    current_room_neighbors = rooms_obj_dft[current_room]

    if next_room in current_room_neighbors.keys():
        traversal_path.append(current_room_neighbors[next_room])

    else:
        short_path = graph.bfs(current_room, next_room)
        while len(short_path) > 1:
            current_room_neighbors = rooms_obj_dft[short_path[0]]
            next_room = short_path[1]

            if next_room in current_room_neighbors.keys():
                traversal_path.append(current_room_neighbors[next_room])
            else:
                traversal_path.append("?")
            short_path.pop(0)
    rooms_list_dft.pop(0)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
