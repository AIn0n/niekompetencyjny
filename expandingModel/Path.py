class Path:
    def __init__(self, length: int, passed_doors: set) -> None:
        self.length = length
        self.passed_doors = passed_doors

        self.flag = 0
        # 0 - in Progress
        # 1 - Target reached
        # -2 - No available path

    def __lt__(self, other):
        return self.length < other.length

    def __gt__(self, other):
        return self.length > other.length

    def __eq__(self, other):
        return self.length == other.length

    def __str__(self):
        out = ""
        for door in self.passed_doors:
            out += str(door) + "||"
        return out
