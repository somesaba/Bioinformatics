import sys, math
import ks, util, bwt, inoutPut
from math import log

"""
    The main function called when main.py is run
    from the command line:

    > python main.py
"""
def main(args):
    #args = sys.argv[1:]
    if len(args) != 3:
        print "Please enter the right number of arguments"
        exit()
    inputFile = open(args[1],'r')
    inputFileReadLine = inputFile.readline()
    inputFileReadLine = inputFileReadLine[1:len(inputFileReadLine)-1]
    S = inoutPut.inputToList(inputFile)
    lengthS = len(S)
    inputFile.close()
    if args[0] == '-bwt':
        print "bwt of:", inputFileReadLine
        newT = util.convertToNumAlphabet(S)
        s_array = ks.cd3(newT)
        S += ["$"]
        b_wt = bwt.bwt(S,s_array)
        outputFile = open(args[2],'w')
        inoutPut.outputToFile(outputFile, b_wt, 'bwt', inputFileReadLine)
        outputFile.close()
        print "length of string:", lengthS
        print "For BWT Check file:", args[2]
    elif args[0] == '-ibwt':
        print "ibwt of:", inputFileReadLine
        rec = bwt.ibwt(S)
        outputFile = open(args[2],'w')
        inoutPut.outputToFile(outputFile, rec,'ibwt', inputFileReadLine)
        outputFile.close()
        print "length of string:", lengthS
        print "For iBWT Check file:", args[2]
            
    else:
        print "You must indicate whether we are doing -btw or -ibtw"
        exit()
    
    pass
if __name__ == '__main__':
    main(sys.argv[1:])
