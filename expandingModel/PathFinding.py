# Probably shouldn't be a separate class
# Should this belong to a Rectangle or Room?
import threading

from expandingModel.Path import Path


class PathFinding:
    def propagatePath(self, current_point, current_room, target, path):
        ##### Pseudocode below #####

        # Target found!
        if current_room.equals(target):
            return path.length

        # Invalid data, current_point must be within current_room.
        if not current_room.contains(current_point):
            # Perhaps use an exception instead?
            return -1
        # No possible further paths, target not found.
        if current_room.available_doors.difference(path.passed_doors).length == 0:
            # Perhaps use an exception instead?
            return -2
        threads = list()

        # For each door out
        for door in room.doors:
            if not door in path.passed_doors:
                # Add new thread to the list
                threads.append(threading.Thread(target=PathFinding.propagatePath(),
                                                args=[door.point, door.room, target,
                                                      Path(path.length + current_point.distance(door),
                                                           path.passed_doors + door)
                                                      ]))

        for thread in threads:
            thread.start()

        results = list()

        for thread in threads:
            thread.join()
            # todo: No such method exists. Figure out a way to obtain return these return values
            # todo: Something to do with threadPools?
            value = thread.return_value
            if value >= 0:
                results.append(value)

        return min(results)
