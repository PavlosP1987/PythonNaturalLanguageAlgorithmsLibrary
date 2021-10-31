from aho_corasick import AhoCorasick
from kmp import KMP

class BakerBird(object):
    def __init__(self, stream, pattern_len):
        self.ac = AhoCorasick()
        for _ in range(pattern_len):
            line = stream.next()
            self.ac.add_patterns(line)
        self.ac.build()

        self.r = {}
        idx = 1

        stream.set_seek()
        for _ in range(pattern_len):
            row = stream.next()
            if row not in self.r.keys():
                self.r[row] = str(idx)
                idx += 1

        stream.set_seek()
        self.kmp = KMP("".join([str(self.r[stream.next()]) for _ in range(pattern_len)]))

    def __call__(self, stream, text_len):
        ret = []
        position = [0,] * text_len
        for i in range(text_len):
            row = stream.next()
            row_R = ["0",] * text_len
            for start, end, keyword in self.ac(row):
                row_R[end-1] = self.r[keyword]

            for idx, R in enumerate(row_R):
                position[idx] = self.kmp.step(R, position[idx])
                if position[idx] is len(self.kmp.keyword):
                    ret.append((i, idx))
                    position[idx] = self.kmp.pi[position[idx]-1]
        return ret