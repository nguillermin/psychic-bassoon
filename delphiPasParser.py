from delphiPasGrammar import grammar

PasParser = grammar

###############################################################################
### Classes
###############################################################################

class Node(list):
    """
    AST node
    """
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, list.__repr__(self))

    @classmethod
    def group(cls, expr):
        def group_action(s, loc, tok):
            try:
                lst = t[0].asList()
            except (IndexError, AttributeError) as e:
                lst = t
            return [cls(lst)]

        return Group(expr).setParseAction(group_action)


def main(argv):
    with open(argv, 'r') as f:
        string = f.read()
    grammar.parseString(string).pprint()


if __name__ == "__main__":
    import pprint, sys

    if len(sys.argv)==1:
        # run tests
        pass
    else:
        main(sys.argv[1])