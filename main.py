import sys

from parser import Parser
from DFA import DFA

# regex = '(0|1(01*0)*1)*'
# regex = '(01*1)*1'
# regex = "(a|b)*abb"
# regex = "(a|b)*"
# regex = "(a*|b*)*"
# regex = '((000)|(001)|(010)|(011)|(100)|(101)|(110)|(111))*'

def showAccepts(regex, testStr):
    sigma = set(regex) - set('()|*')
    tokens = Parser.tokenize(regex + '#')

    rpn = Parser.infixToPostfix(tokens)
    st, positions = Parser.syntaxTreeFromRPN(rpn)
    followpos = st.getFollowpos()

    dfa = st.toDFA(followpos, positions, sigma)
    print(dfa.accepts(testStr))

    dfa.visualize()

    eqCls = dfa.findEquivalenceClasses(sigma)
    dfa.mergeEquivalentStates(eqCls)
    dfa.visualize(fname='fsm1.gv')

    print(dfa.accepts(testStr))


def showMinimization():
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

    dfa.visualize()

    eqCls = dfa.findEquivalenceClasses(sigma)
    dfa.mergeEquivalentStates(eqCls)
    dfa.visualize(fname='fsm1.gv')

def showMinimization4():
    tt = {
        frozenset(['a']): {
            '0': frozenset(['b']),
            '1': frozenset(['c'])
        },
        frozenset(['b']): {
            '0': frozenset(['e']),
            '1': frozenset(['f'])
        },
        frozenset(['c']): {
            '0': frozenset(['a']),
            '1': frozenset(['a'])
        },
        frozenset(['d']): {
            '0': frozenset(['f']),
            '1': frozenset(['e'])
        },
        frozenset(['e']): {
            '0': frozenset(['d']),
            '1': frozenset(['f'])
        },
        frozenset(['f']): {
            '0': frozenset(['d']),
            '1': frozenset(['e'])
        }
    }
    sigma = set(['0', '1'])
    start = 'a'
    end = set([frozenset(['e']), frozenset(['f'])])
    dfa = DFA(tt, start, end)

    dfa.visualize()

    eqCls = dfa.findEquivalenceClasses(sigma)
    dfa.mergeEquivalentStates(eqCls)
    dfa.visualize(fname='fsm1.gv')

# showAccepts(regex, '000111')
# showMinimization()
# showMinimization4()

if len(sys.argv) == 3:
    showAccepts(sys.argv[1], sys.argv[2])
else:
    print("")

