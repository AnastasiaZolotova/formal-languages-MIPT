import dataclasses


@dataclasses.dataclass
class Rule:
    left_part: str
    right_part: str


@dataclasses.dataclass(eq=True, frozen=True)
class Situation:
    left_side: str
    right_side: str
    point_coord: int
    offset: int


INITIAL_SITUATION = Situation('#', 'S', 0, 0)
TERMINAL_SITUATION = Situation('#', 'S', 1, 0)


class EarlyParser:

    def __init__(self, rules: list):
        self.rules = [Rule(left_part='#', right_part='S')] + rules
        self.situations: list[set[Situation]] = []
        self.word = ""

    def check(self, w: str):
        self.word = w
        self.situations = [{INITIAL_SITUATION} if not _ else set() for _ in range(len(w) + 1)]
        for i, situation in enumerate(self.situations):
            self.scan(i)
            old_size = -1
            while old_size != len(situation):
                old_size = len(situation)
                self.complete(i)
                self.predict(i)

        return TERMINAL_SITUATION in self.situations[-1]

    def scan(self, i):
        if not i:
            return
        for item in self.situations[i - 1]:
            if item.point_coord < len(item.right_side) and item.right_side[item.point_coord] == self.word[i - 1]:
                new_trans = Situation(item.left_side, item.right_side, item.point_coord + 1, item.offset)
                self.situations[i].add(new_trans)

    def predict(self, j):
        new = set()
        for item in self.situations[j]:
            if item.point_coord == len(item.right_side):
                continue
            waiting_left = item.right_side[item.point_coord]
            for rule in self.rules:
                if rule.left_part == waiting_left:
                    new_trans = Situation(rule.left_part, rule.right_part, 0, j)
                    new.add(new_trans)
        self.situations[j].update(new)

    def complete(self, k):
        new = set()
        for compItem in self.situations[k]:
            if compItem.point_coord < len(compItem.right_side):
                continue
            for nextItem in self.situations[compItem.offset]:
                if nextItem.point_coord < len(nextItem.right_side) and \
                        nextItem.right_side[nextItem.point_coord] == compItem.left_side:
                    transitives = Situation(nextItem.left_side, nextItem.right_side, nextItem.point_coord + 1,
                                          nextItem.offset)
                    new.add(transitives)
        self.situations[k].update(new)
