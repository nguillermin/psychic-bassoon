from delphiPasParser import titleAndInterface # Until the parser is fully functional, just the parts that work
from delphiDfmParser import DfmParser

def main(arg):
    filename = os.path.splitext(os.path.split(arg)[1])[0]

    with open('../Delphi/'+filename+'.dfm', 'r', encoding='ascii') as f:
        string = f.read()
    parseResults = DfmParser.parseString(string)
    dfmComponents = [n[0][0] for n in parseResults[2:]]
    
    with open('../Delphi/'+filename+'.pas', 'r', encoding='utf8') as f:
        string = f.read()
    parseResults = titleAndInterface.parseString(string).pprint()


if __name__ == "__main__":
    import pprint, os, sys
    if len(sys.argv)==1:
        raise ValueError("No arguments specified")
        exit()
    else:
        main(sys.argv[1])