import delphiPasGrammar

PasParser = delphiPasGrammar.grammar

###############################################################################
### Classes
###############################################################################


class Node():
    """
    AST node
    """
    def __eq__(self, other):
        return self.__class__ == other.__class__ # And contents?


    # def __repr__(self):
    #     return '%s(%s)' % (self.__class__.__name__, Node.__repr__(self))


    @classmethod
    def group(cls, expr):
        def group_action(s, loc, tok):
            try:
                lst = tok[0].asList()
            except (IndexError, AttributeError) as e:
                lst = tok
            return Node(lst)

        return Group(expr).setParseAction(group_action)


def main(argv):
    grammarTypes = [item for item in dir(delphiPasGrammar) if item[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and item[0:2]!='__']
    # print(grammarTypes)
    art = [type()]


    # with open(argv, 'r') as f:
    #     string = f.read()
    # grammar.parseString(string).pprint()


if __name__ == "__main__":
    import pprint, sys

    if len(sys.argv)==1:
        main('shim')
    else:
        main(sys.argv[1])