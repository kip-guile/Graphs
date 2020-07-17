from room import Room
from player import Player
from world import World
from util import Stack

import random
from ast import literal_eval

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

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
stack = Stack()
graph = {}

while len(graph) < 500 and len(traversal_path) < 2000:
    print(traversal_path)
    current_room = player.current_room.id

    if current_room not in graph:
        current_exits = {}

        for exit in player.current_room.get_exits():
            current_exits[exit] = '?'
        graph[current_room] = current_exits

    current_exits = graph[current_room]

    if 'n' in current_exits and current_exits['n'] == '?':
        player.travel('n')
        traversal_path.append('n')
        next_room = player.current_room.id
        current_exits['n'] = next_room

        if next_room not in graph:
            next_room_exits = {}

            for exit in player.current_room.get_exits():
                next_room_exits[exit] = '?'

            next_room_exits['s'] = current_room
            graph[next_room] = next_room_exits
        else:
            graph[next_room]['s'] = current_room
        stack.push('s')

    elif 'e' in current_exits and current_exits['e'] == '?':
        player.travel('e')
        traversal_path.append('e')
        next_room = player.current_room.id
        current_exits['e'] = next_room

        if next_room not in graph:
            next_room_exits = {}

            for exit in player.current_room.get_exits():
                next_room_exits[exit] = '?'

            next_room_exits['w'] = current_room
            graph[next_room] = next_room_exits
        else:
            graph[next_room]['w'] = current_room
        stack.push('w')

    elif 's' in current_exits and current_exits['s'] == '?':
        player.travel('s')
        traversal_path.append('s')
        next_room = player.current_room.id
        current_exits['s'] = next_room

        if next_room not in graph:
            next_room_exits = {}

            for exit in player.current_room.get_exits():
                next_room_exits[exit] = '?'

            next_room_exits['n'] = current_room
            graph[next_room] = next_room_exits
        else:
            graph[next_room]['n'] = current_room
        stack.push('n')

    elif 'w' in current_exits and current_exits['w'] == '?':
        player.travel('w')
        traversal_path.append('w')
        next_room = player.current_room.id
        current_exits['w'] = next_room

        if next_room not in graph:
            next_room_exits = {}

            for exit in player.current_room.get_exits():
                next_room_exits[exit] = '?'

            next_room_exits['e'] = current_room
            graph[next_room] = next_room_exits
        else:
            graph[next_room]['e'] = current_room
        stack.push('e')

    else:
        goBack = stack.pop()
        if goBack is None:
            break

        player.travel(goBack)
        traversal_path.append(goBack)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
