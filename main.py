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
        self._rules: list[Rule] = [Rule(left_part='#', right_part='S')] + rules
        self._situations: list[set[Situation]] = []
        self._word: str = ""

    def check(self, w: str) -> bool:
        self._word = w
        self._situations = [{INITIAL_SITUATION} if not _ else set() for _ in range(len(w) + 1)]
        for i, situation in enumerate(self._situations):
            self._scan(i)
            old_size = -1
            while old_size != len(situation):
                old_size = len(situation)
                self._complete(i)
                self._predict(i)

        return TERMINAL_SITUATION in self._situations[-1]

    def _scan(self, i) -> None:
        if not i:
            return
        for item in self._situations[i - 1]:
            if item.point_coord < len(item.right_side) and item.right_side[item.point_coord] == self._word[i - 1]:
                new_trans = Situation(item.left_side, item.right_side, item.point_coord + 1, item.offset)
                self._situations[i].add(new_trans)

    def _predict(self, j) -> None:
        new = set()
        for item in self._situations[j]:
            if item.point_coord == len(item.right_side):
                continue
            waiting_left = item.right_side[item.point_coord]
            for rule in self._rules:
                if rule.left_part == waiting_left:
                    new_trans = Situation(rule.left_part, rule.right_part, 0, j)
                    new.add(new_trans)
        self._situations[j].update(new)

    def _complete(self, k) -> None:
        new = set()
        for compItem in self._situations[k]:
            if compItem.point_coord < len(compItem.right_side):
                continue
            for nextItem in self._situations[compItem.offset]:
                if nextItem.point_coord < len(nextItem.right_side) and \
                        nextItem.right_side[nextItem.point_coord] == compItem.left_side:
                    transitives = Situation(nextItem.left_side, nextItem.right_side, nextItem.point_coord + 1,
                                          nextItem.offset)
                    new.add(transitives)
        self._situations[k].update(new)
