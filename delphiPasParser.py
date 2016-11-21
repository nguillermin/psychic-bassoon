import delphiPasGrammar

PasParser = delphiPasGrammar.grammar

###############################################################################
### Classes
###############################################################################


class Node(list):
    """
    AST node
    """
    def __eq__(self, other):
        return self.__class__ == other.__class__ # And contents?


    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, Node.__repr__(self))


    @classmethod
    def group(cls, expr):
        def group_action(s, loc, tok):
            try:
                lst = tok[0].asList()
            except (IndexError, AttributeError) as e:
                lst = tok
            return Node(lst)

        return Group(expr).setParseAction(group_action)


def makeNode(_typeName):
    node = type(str(_typeName)+"Node", (Node,), {})


def main(argv):
    grammarTypes = [item for item in dir(delphiPasGrammar) if 
            item[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and item[0:2]!='__']

    art = {x: type(str(x)+"Node", (Node,), {}) for x in grammarTypes}

    for key in art.keys():
        globals()[key] = art[key].group(globals()[key])

    if argv=='':
        exit()
    else:
        with open(argv[1], 'rb') as f:
            detect = chardet.detect(f.read())

        print('Encoding used: ' + detect['encoding'] + ' with confidence: ' + repr(detect['confidence']))
        with open(argv[1],'r', encoding=detect['encoding']) as f:
            string = f.read()
        grammar.parseString(string).pprint()


if __name__ == "__main__":
    from delphiPasGrammar import *
    import pprint, sys, chardet

    if len(sys.argv)==1:
        main('')
    else:
        main(sys.argv)
