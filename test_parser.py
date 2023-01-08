import dataclasses
import pytest
from main import EarlyParser, Rule


@dataclasses.dataclass
class Case:
    rules: list[Rule]
    words: list[str]
    answers: list[bool]


TEST_CASES = [
    Case(
        rules=[
            Rule("S", "aSb"),
            Rule("S", "a")
        ],
        words=[
            "ab",
            "aab",
            "aaabb",
            "aabb",
            "baaabb"
        ],
        answers=[False, True, True, False, False]
    ),
    Case(
        rules=[
            Rule("S", ""),
            Rule("S", "aS"),
            Rule("S", "ASb"),
            Rule("A", "bA"),
            Rule("A", "")
        ],
        words=[
            "",
            "aaaaabbbbaaaaa",
            "aabbaabbb",
            "bbbbbbab",
            "abaaaa"
        ],
        answers=[True, False, True, True, False]
    )
]


@pytest.mark.parametrize("case", TEST_CASES)
def test_general(case):
    parser = EarlyParser(case.rules)
    assert [parser.check(word) for word in case.words] == case.answers
