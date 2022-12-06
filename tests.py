import unittest
from formal_languages import max_possible_subword_of_expr
 
 
class MyTestCase(unittest.TestCase):
    def test_number0(self):
        expression = "ab.*"
        line = "cccababacc"
        result = 5
        self.assertEqual(max_possible_subword_of_expr(expression, line), result)  # add assertion here
 
    def test_number1(self):
        expression = "ab+c.aba.*.bac.+.+*"
        line = "bbaaacaaabacbb"
        result = 5
        self.assertEqual(max_possible_subword_of_expr(expression, line), result)  # add assertion here
 
    def test_number2(self):
        expression = "a**"
        line = "aacb"
        result = 2
        self.assertEqual(max_possible_subword_of_expr(expression, line), result)  # add assertion here
 
    def test_number3(self):
        expression = "c*a."
        line = "acccaacbaccccccabcca"
        result = 7
        self.assertEqual(max_possible_subword_of_expr(expression, line), result)  # add assertion here
 
    def test_number4(self):
        expression = "ab+*c."
        line = "cacacc"
        result = 2
        self.assertEqual(max_possible_subword_of_expr(expression, line), result)  # add assertion here
 
    def test_number5(self):
        expression = "ab.c*."
        line = "cccacabb"
        result = 3
        self.assertEqual(max_possible_subword_of_expr(expression, line), result)  # add assertion here
 
    def test_number6(self):
        expression = "ab+c.c+*"
        line = "abccaabca"
        result = 4
        self.assertEqual(max_possible_subword_of_expr(expression, line), result)  # add assertion here
 
    def test_number7(self):
        expression = "ab*+"
        line = "cccc"
        result = 0
        self.assertEqual(max_possible_subword_of_expr(expression, line), result)  # add assertion here
 
 
if __name__ == '__main__':
    unittest.main()