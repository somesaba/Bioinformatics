# main.py
# ----------
# HMM_TMRCA Project
# Licensing Information: Please do not distribute.
# You are free to use and extend these code for educational purposes.
# ProblemSet written by professor Yun S. Song
# Solution and code written by Jae Young Ryoo (jay.ryoo@gmail.com) and Saba Khalilnaji

import sys, math, hmm, algorithms, util, parser, fileHandler

def main(args):
    if(len(args) != 2):
        print "Error. main.py needs two arguments"
        print "Example: python main.py sequences.fasta initial_parameters.txt"
        exit()
    s = [1,2,3,4]
    stateMapper = {1:0.32, 2:1.75, 3:4.54, 4:9.40}
    pParser = parser.pparser()
    parameters = pParser.parse_Parameters(args[1])
    p = parameters[0]
    a = parameters[1]
    e = parameters[2]
    q = ['I', 'D']
    x = util.compareSequences(args[0])
    markovModel = hmm.HMM(False,s, q, a, e, p)
    
    newModel = algorithms.baum_welch_log(markovModel, [x][:], 10)
    fileHandler.outputEstimatedParameters(newModel, 'estimated_parameters.txt')
    likelihoods = [algorithms.forward_log(markovModel, x),algorithms.forward_log(newModel, x)]
    fileHandler.outputLikelihoods(likelihoods, 'likelihoods.txt')

    decodings_initial = algorithms.decodings(markovModel, x[:])
    fileHandler.outputDecodings(decodings_initial, 'decodings_initial.txt')
    
    decodings_estimated = algorithms.decodings(newModel, x[:])
    fileHandler.outputDecodings(decodings_estimated, 'decodings_estimated.txt')
            
if __name__== '__main__':
    main(sys.argv[1:])
