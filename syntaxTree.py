from collections import defaultdict
from DFA import DFA

class SyntaxTree:
    def __init__(self, 
                 value,
                 position,
                 left,
                 right,
                 nullable,
                 firstpos,
                 lastpos):
        self.value = value
        self.position = position
        self.left = left
        self.right = right
        self.nullable = nullable
        self.firstpos = firstpos
        self.lastpos = lastpos

    def getFollowpos(self):
        result = defaultdict(frozenset)
        return self._getFollowpos(result)

    
    def _getFollowpos(self, result):
        if self.value == 'CONCAT':
            for i in self.left.lastpos:
                result[i] = result[i].union(self.right.firstpos)
        elif self.value == '*':
            for i in self.lastpos:
                result[i] = result[i].union(self.firstpos)

        if self.left is not None:
            result = self.left._getFollowpos(result)
        if self.right is not None:
            result = self.right._getFollowpos(result)

        return result

    def toDFA(self, followpos, positions, sigma):
        s0 = self.firstpos
        dstates = {s0: False}
        dtran = defaultdict(dict)
        s = self._getNextState(dstates)
        start = s
        ends = []
        maxState = max(positions)
        while True:
            dstates[s] = True
            if maxState in s:
                ends.append(s)
            for a in sigma:
                u = frozenset()
                for p in s:
                    if positions[p] == a:
                        u = u.union(followpos[p])
                
                if not u in dstates:
                    dstates[u] = False

                dtran[s][a] = u
            end = s
            s = self._getNextState(dstates)
            if s is None:
                break
        
        return DFA(dtran, start, ends)
        

    def _getNextState(self, dstates):
        for k, v in dstates.items():
            if not v:
                return k
        return None

