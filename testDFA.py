import unittest
from parser import tokenize, infixToPostfix, syntaxTreeFromRPN
from DFA import DFA

class TestDFA(unittest.TestCase):
    def testConstruct(self):
        patterns = [
            '(0|1(01*0)*1)*',
            '(01*1)*1',
            '(a|b)*abb',
            '(a|b)*',
            '(a*|b*)*',
            '((000)|(001)|(010)|(011)|(100)|(101)|(110)|(111))*'
        ]
        for p in patterns:
            sigma = set(p) - set('()|*')
            tokens = tokenize(p + '#')
            rpn = infixToPostfix(tokens)
            st, positions = syntaxTreeFromRPN(rpn)
            followpos = st.getFollowpos()
            dfa = st.toDFA(followpos, positions, sigma)

    def getCases(self):
        tests = {
            '(0|1(01*0)*1)*' : { # binary numbers divisible by 3
                '': True,
                '0': True,
                '011': True,
                '110':True,
                '1001':True,
                '1100':True,
                '1111':True,
                '10010':True,
                'lupa': False,
                '111': False
            },
            '(01*1)*1': {
                '': False,
                '1': True,
                '011': True,
                '1001': False
            },
            '(a|b)*abb': {
                '': False,
                'abb': True,
                'aabb': True,
                'babb': True,
                'ababb':True,
                'ab': False,
            },
            '(a|b)*': {
                '': True,
                'a': True,
                'b': True,
                'ab': True,
                'ba': True,
                'pupa': False, 
            },
            '(a*|b*)*': {
                '': True,
                'a': True,
                'b': True,
                'ab': True,
                'ba': True,
                'pupa': False, 
            },
            '((000)|(001)|(010)|(011)|(100)|(101)|(110)|(111))*': {
                '': True,
                '0': False,
                '10': False,
                '111': True,
                '101': True,
                '1111': False,
                '010001': True
            }
        }

        return tests

    def testAccepts(self):
        for pattern, testCases in self.getCases().items():
            sigma = set(pattern) - set('()|*')
            tokens = tokenize(pattern + '#')
            rpn = infixToPostfix(tokens)
            st, positions = syntaxTreeFromRPN(rpn)
            followpos = st.getFollowpos()
            dfa = st.toDFA(followpos, positions, sigma)
            for t, accepts in testCases.items():
                self.assertEqual(dfa.accepts(t), accepts)

    def testMinimizeAndAccepts(self):
        for pattern, testCases in self.getCases().items():
            sigma = set(pattern) - set('()|*')
            tokens = tokenize(pattern + '#')
            rpn = infixToPostfix(tokens)
            st, positions = syntaxTreeFromRPN(rpn)
            followpos = st.getFollowpos()
            dfa = st.toDFA(followpos, positions, sigma)
            eqCls = dfa.findEquivalenceClasses(sigma)
            dfa.mergeEquivalentStates(eqCls)
            for t, accepts in testCases.items():
                self.assertEqual(dfa.accepts(t), accepts)

    def testMinimize(self):
        # https://en.wikipedia.org/wiki/DFA_minimization
        tt = {
            frozenset(['a']): {
                '0': frozenset(['b']),
                '1': frozenset(['c'])
            },
            frozenset(['b']): {
                '0': frozenset(['a']),
                '1': frozenset(['d'])
            },
            frozenset(['c']): {
                '0': frozenset(['e']),
                '1': frozenset(['f'])
            },
            frozenset(['d']): {
                '0': frozenset(['e']),
                '1': frozenset(['f'])
            },
            frozenset(['e']): {
                '0': frozenset(['e']),
                '1': frozenset(['f'])
            },
            frozenset(['f']): {
                '0': frozenset(['f']),
                '1': frozenset(['f'])
            }
        }
        sigma = set(['0', '1'])
        start = 'a'
        end = set([frozenset(['c']), frozenset(['d']), frozenset(['e'])])
        dfa = DFA(tt, start, end)

        self.assertEqual(len(dfa.ends), 3)
        self.assertEqual(len(dfa.transitions), 6)
        
        eqCls = dfa.findEquivalenceClasses(sigma)
        dfa.mergeEquivalentStates(eqCls)

        self.assertEqual(len(dfa.ends), 1)
        self.assertEqual(len(dfa.transitions), 3)