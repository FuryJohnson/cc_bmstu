from collections import defaultdict
from queue import Queue
from graphviz import Digraph

class DFA:
    def __init__(self, transitions, start, ends):
        self.transitions = transitions
        self.start = start
        self.ends = ends
    
    def accepts(self, s):
        state = self.start
        for ch in s:
            if ch not in self.transitions[state]:
                return False
            state = self.transitions[state][ch]
        
        return state in self.ends

    def visualize(self, fname='fsm.gv'):
        def _frozensetStr(fs):
            s = '{'
            for v in fs:
                s += ' {}, '.format(v)
            return s + '}'

        f = Digraph('finite_state_machine', filename=fname)
        f.attr(rankdir='LR')

        f.attr('node', style='invis')
        f.node('start')

        f.attr('node', shape='doublecircle', style='solid')
        for end in self.ends:
            f.node(_frozensetStr(end))

        f.attr('node', shape='circle')
        f.edge('start', _frozensetStr(self.start), label='start')
        for s0, v in self.transitions.items():
            for ch, s1 in v.items():
                f.edge(_frozensetStr(s0), _frozensetStr(s1), label=ch)
        
        f.view()

    def findEquivalenceClasses(self, sigma):
        """http://neerc.ifmo.ru/wiki/index.php?title=%D0%9C%D0%B8%D0%BD%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D0%94%D0%9A%D0%90,_%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%A5%D0%BE%D0%BF%D0%BA%D1%80%D0%BE%D1%84%D1%82%D0%B0_(%D1%81%D0%BB%D0%BE%D0%B6%D0%BD%D0%BE%D1%81%D1%82%D1%8C_O(n_log_n))
        """
        Cls = self._init_class()
        inv = self._init_inv()
        Q = self.transitions.keys()
        F = set(self.ends)
        queue = Queue()
        P = [F, Q-F]

        for c in sigma:
            queue.put((F, c))
            queue.put((Q-F, c))
    
        while not queue.empty():
            C, a = queue.get()
            involved = {}
            for q in C:
                for r in inv[q][a]:
                    i = Cls[r]
                    if i not in involved:
                        involved[i] = set()
                    involved[i].add(r)
            for i in involved.keys():
                if len(involved[i]) < len(P[i]):
                    P.append(set())
                    j = len(P) - 1
                    for r in involved[i]:
                        P[i].remove(r)
                        P[j].add(r)
                    if len(P[j]) > len(P[i]):
                        tmp = P[i]
                        P[i] = P[j]
                        P[j] = tmp
                    for r in P[j]:
                        Cls[r] = j
                    for c in sigma:
                        queue.put((P[j], c))
        return P
    
    def _init_inv(self):
        result = defaultdict(lambda: defaultdict(list))
        for s0, v in self.transitions.items():
            for ch, s1 in v.items():
                result[s1][ch].append(s0)
        return result

    def _init_class(self):
        result = {}
        F = set(self.ends)
        for r in self.transitions.keys():
            if r in F:
                result[r] = 0
            else:
                result[r] = 1
        return result

    def mergeEquivalentStates(self, classes):
        ends = set([x for x in self.ends])
        for cls in classes:
            if len(cls) > 1:
                newstate = frozenset()
                for state in cls:
                    newstate = newstate.union(state)
                self._updateIn(cls, newstate)
                self._updateOut(cls, newstate)

                if frozenset(self.start) in cls:
                    self.start = newstate
                
                for state in cls:
                    if state in self.ends:
                        ends.add(newstate)
                        ends.remove(state)

                self._removeEqualStates(cls)
        self.ends = ends

    def _updateIn(self, cls, newstate):
        """update connections that go to states in cls
        """
        for s0, v in self.transitions.items():
            for ch, s1 in v.items():
                if s1 in cls:
                    self.transitions[s0][ch] = newstate

    def _updateOut(self, cls, newstate):
        """update connections that go from states in cls
        """
        self.transitions[newstate] = {}
        for s0, v in self.transitions.items():
            for ch, s1 in v.items():
                if s0 in cls:
                    self.transitions[newstate][ch] = s1

    def _removeEqualStates(self, cls):
        for state in cls:
            del self.transitions[state]

