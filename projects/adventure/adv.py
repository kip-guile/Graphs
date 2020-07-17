from room import Room
from player import Player
from world import World
from util import Stack, Queue

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
# and len(traversal_path) < 2000
# while graph has not been traversed and all
while len(graph) < 500:
    print(stack.stack)
    # build graph
    # set current room to be room player is in
    current_room = player.current_room.id

    # find room exits
    if current_room not in graph:
        # if current room is not in graph, then set current exits to {}
        current_exits = {}

        # loop through exits array, creating a key in current exits dict with value '?'
        for exit in player.current_room.get_exits():
            current_exits[exit] = '?'
        # initial graph in the form 0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
        graph[current_room] = current_exits

    # get object with available exits
    current_exits = graph[current_room]

    # move north if possible
    # check if the room north exists and has never been visited
    if 'n' in current_exits and current_exits['n'] == '?':
        # if so, move north
        player.travel('n')
        # append n to traversal array
        traversal_path.append('n')
        # next room is the id of current room we are in because we moved
        next_room = player.current_room.id
        # change value of current exits[n] from ? to room id to show it has been visited
        current_exits['n'] = next_room

        # add next room to graph
        if next_room not in graph:
            next_room_exits = {}
            # loop through exits array, creating a key in current exits dict with value '?'
            for exit in player.current_room.get_exits():
                next_room_exits[exit] = '?'
            # change value of current exits[s] from ? to room id to show it has been visited
            next_room_exits['s'] = next_room
            # add room to graph
            graph[next_room] = next_room_exits
        else:
            graph[next_room]['s'] = next_room
        # push opposite direction into stack
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
    # go back if there is no direction to move in
    else:
        # the opposite direction is in stack so pop to get it
        goBack = stack.pop()
        # break is stack is empty
        if goBack is None:
            break
        # move in popped direction to go back
        player.travel(goBack)
        # add popped direction to traversal path
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
