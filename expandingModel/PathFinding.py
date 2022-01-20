# Probably shouldn't be a separate class
# Should this belong to a Rectangle or Room?
import threading

from Path import Path
from Room import Room
from figures.figures import Point


def propagatePath(current_point: Point, current_room: Room, target, path):
    print("\n#######START", current_room, "#######")
    ##### Pseudocode below #####
    print("Current point:", current_point)
    print("Current room:", current_room)
    print("Target room:", target)
    print("Path: ", path.__str__())

    # Target found!
    if current_room == target:
        print("TARGET REACHED, TRAVELED DISTANCE: ", path.length)
        path.flag = 1
        return path

    # Invalid data, current_point must be within current_room.
    # if not current_room.Rect.contains(current_point):
    # Perhaps use an exception instead?
    #    return -1
    # No possible further paths, target not found.
    available_doors = current_room.doors.difference(path.passed_doors)
    print("Available doors:", end=" ")
    for door in available_doors:
        print(door, end=", ")
    print()

    if len(available_doors) == 0:
        # Perhaps use an exception instead?
        print("NO PATHS AVAILABLE, TERMINATE")
        path.flag = -2
        return path

    results = list()

    tempPassed = set()
    # For each door out
    for door in available_doors:
        # The path starting from this door
        tempPassed = path.passed_doors.copy()
        tempPassed.add(door)
        # Returns the minimal path starting from this door
        result = propagatePath(
            door.coords,
            door.leadsTo,
            target,
            Path(path.length + current_point.distance(door.coords), tempPassed),
        )
        if result.flag >= 0:
            results.append(result)

    print("#######END", current_room, "#######")

    # No paths were found
    if len(results) == 0:
        path.flag = -2
        return path
    return min(results)
