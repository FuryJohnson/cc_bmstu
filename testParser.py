import unittest
from parser import tokenize, infixToPostfix

class TestParsing(unittest.TestCase):
    def testTokenize(self):
        testCases = [
            '(0|1(01*0)*1)*',
            '(01*1)*1',
            '(a|b)*abb',
            '(a|b)*',
            '(a*|b*)*'
        ]
        expected = [
            ['(', '0', '|', '1', 'CONCAT', '(', '0', 'CONCAT', '1', '*', 'CONCAT', '0', ')', '*', 'CONCAT', '1', ')', '*'],
            ['(', '0', 'CONCAT', '1', '*', 'CONCAT', '1', ')', '*', 'CONCAT', '1'],
            ['(', 'a', '|', 'b', ')', '*', 'CONCAT', 'a', 'CONCAT', 'b', 'CONCAT', 'b'],
            ['(', 'a', '|', 'b', ')', '*'],
            ['(', 'a', '*', '|', 'b', '*', ')', '*']
        ]
        for t, e in zip(testCases, expected):
            self.assertEqual(tokenize(t), e)

    def testRPN(self):
        testCases = [
            ['(', '0', '|', '1', 'CONCAT', '(', '0', 'CONCAT', '1', '*', 'CONCAT', '0', ')', '*', 'CONCAT', '1', ')', '*', 'CONCAT', '#'],
            ['(', '0', 'CONCAT', '1', '*', 'CONCAT', '1', ')', '*', 'CONCAT', '1', 'CONCAT', '#'],
            ['(', 'a', '|', 'b', ')', '*', 'CONCAT', 'a', 'CONCAT', 'b', 'CONCAT', 'b', 'CONCAT', '#'],
            ['(', 'a', '|', 'b', ')', '*', 'CONCAT', '#'],
            ['(', 'a', '*', '|', 'b', '*', ')', '*', 'CONCAT', '#']
        ]
        expected = [
            ['0', '1', '0', '1', '*', 'CONCAT', '0', 'CONCAT', '*', 'CONCAT', '1', 'CONCAT', '|', '*', '#', 'CONCAT'],
            ['0', '1', '*', 'CONCAT', '1', 'CONCAT', '*', '1', 'CONCAT', '#', 'CONCAT'],
            ['a', 'b', '|', '*', 'a', 'CONCAT', 'b', 'CONCAT', 'b', 'CONCAT', '#', 'CONCAT'],
            ['a', 'b', '|', '*', '#', 'CONCAT'],
            ['a', '*', 'b', '*', '|', '*', '#', 'CONCAT']
        ]
        for t, e in zip(testCases, expected):
            self.assertEqual(infixToPostfix(t), e) 

if __name__ == '__main__':
    unittest.main()
