class SuffixNode(object):
def __init__(self, text):

self.children = {}

self.parent = None

self.suffix_link = None

self.i_from = 0

self.i_to = 0

self.text = text



@property

def length(self):

return self.i_to - self.i_from



def add(self, i_from, i_to):

child = SuffixNode(self.text)

child.i_from = i_from

child.i_to = i_to

child.parent = self

self[self.text[i_from]] = child

