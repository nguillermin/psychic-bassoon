from delphiPasParser import PasParser
from delphiDfmParser import DfmParser

def main(argv):
    with open(argv, 'r') as f:
        string = f.read()
    grammar.parseString(string).pprint()


if __name__ == "__main__":
    import pprint, sys
    main(sys.argv[1])