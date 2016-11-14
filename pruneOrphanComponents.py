from delphiPasParser import titleAndInterface # Until the parser is fully functional, just the parts that work
from delphiDfmParser import DfmParser

import os, sys
import chardet

def main(arg):
    filename = os.path.splitext(os.path.split(arg)[1])[0]

    dfmFile = '../Delphi/'+filename+'.dfm'
    pasFile = '../Delphi/'+filename+'.pas'

    f = open(dfmFile,'rb')
    guess = chardet.detect(f.read(1000))
    print(guess)
    if guess['confidence']==1.0:
        codec = guess['encoding']
    else:
        print('Not sure on '+filename+'.dfm encoding, exiting.')
        exit()
    f.close()

    with open(dfmFile, 'rb') as f:
        string = f.read()
    parseResults = DfmParser.parseString(string.decode('utf-8'))
    dfmComponents = [n[0][0] for n in parseResults[2:]]
    
    f = open(pasFile,'rb')
    guess = chardet.detect(f.read(1000))
    print(guess)
    if guess['confidence']==1.0:
        codec = guess['encoding']
    else:
        print('Not sure on '+filename+'.dfm encoding, exiting.')
        exit()
    f.close()

    with open(pasFile, 'rb') as f:
        string = f.read()
    parseResults = titleAndInterface.parseString(string.decode('utf-8'))
    print(parseResults.dump())


if __name__ == "__main__":
    if len(sys.argv)==1:
        raise ValueError("No arguments specified")
        exit()
    else:
        main(sys.argv[1])