# algorithms.py
# ----------
# HMM_TMRCA Project
# Licensing Information: Please do not distribute.
# You are free to use and extend these code for educational purposes.
# ProblemSet written by professor Yun S. Song
# Solution and code written by Jae Young Ryoo (jay.ryoo@gmail.com) and Saba Khalilnaji

import sys, math, util, hmm

#######################################################################################
"""
Helper Methods

logSum: takes in a list of logs and performs an efficient sum of their exponentials
using the identity: R = P + log(1 + exp(Q - P)), where P = log(p), Q = log(q)

INPUT: (list) a list of log values
OUTPUT: (Float) an efficient sum of their exponentials
"""

def logSum(listToSum):
    if len(listToSum) == 0:
        print "Error: Transition Probability of 0"
        return
    sumToReturn = listToSum[0]
    for i in range(1, len(listToSum)):
        sumToReturn = sumToReturn + math.log(1 + math.exp(listToSum[i] - sumToReturn))
    return sumToReturn

"""
posterior_decoding
INPUT: HMM Model, (list) emissions
OUTPUT: (list) of posteriors

primarily used for testing, not part of project code
"""

def posterior_decoding(model, emissions):
    forwardList = getForwardList_log(model, emissions)
    forwardLog = logSum([forwardList[len(forwardList)-1][state] for state in model.getStates()])
    backwardList = getBackwardList_log(model, emissions)
    posterior = []
    
    for i in range(len(emissions)):
        counterOfStates = util.Counter()
        for s in model.getStates():
            counterOfStates[(i,s)] = (forwardList[i][s] + backwardList[i][s]) - forwardLog
        posterior.append(counterOfStates.argMax()[1])

    return posterior

#######################################################################################
"""
The forward algorithm
This calculates P(X|Theta)
f_k is a counter where the keys are k
a list of f_k represents the passage of time
where the index is t
"""
def forward(model, emissions):
    f = util.Counter()
    for state in model.getStates():
        f[state] = model.p(state)*model.e(state, emissions[0])  
    for b in emissions[1:]:
        f_next = util.Counter()
        for state_l in model.getStates():
            f_next[state_l] = model.e(state_l, b) * sum([model.a(state_k, state_l)*f[state_k] for state_k in model.getStates()])
        f = f_next.copy()
    return f.totalCount()

"""
The forward algorithm in log space
This calculates P(X|Theta)
f_k is a counter where the keys are k
a list of f_k represents the passage of time
where the index is t
"""

def forward_log(model, emissions):
    F = util.Counter()
    for state in model.getStates():
        F[state] = model.p_log(state) + model.e_log(state, emissions[0])  
    for b in emissions[1:]:
        F_next = util.Counter()
        for state_l in model.getStates():
            F_next[state_l] = model.e_log(state_l, b) + logSum([model.a_log(state_k, state_l) + F[state_k] for state_k in model.getStates()])
        F = F_next.copy()
    return logSum(F.values())
    
"""
For the baum-welch algorithm we need f_k(t)
for every state k and for every t in len(emission)
instead of recalculating the same previous values
again we're just gonna store them sequentially
in a list of dictionaries
"""
def getForwardList(model, emissions):
    f = util.Counter()
    for state in model.getStates():
        f[state] = model.p(state)*model.e(state, emissions[0])
    forwardList = [f]  
    for b in emissions[1:]:
        f_next = util.Counter()
        for state_l in model.getStates():
            f_next[state_l] = model.e(state_l, b) * sum([model.a(state_k, state_l)*f[state_k] for state_k in model.getStates()])
        f = f_next.copy()
        forwardList.append(f)
    return forwardList

"""
getForwardList_log:
The same thing as getForwardList, but returns log values
"""
def getForwardList_log(model, emissions):
    F = util.Counter()
    for state in model.getStates():
        F[state] = model.p_log(state) + model.e_log(state, emissions[0])
    forwardList_log = [F]  
    for b in emissions[1:]:
        F_next = util.Counter()
        for state_l in model.getStates():
            F_next[state_l] = model.e_log(state_l, b) + logSum([model.a_log(state_k, state_l) + F[state_k] for state_k in model.getStates()])
        F = F_next.copy()
        forwardList_log.append(F)
    return forwardList_log


#######################################################################################    
"""
The backward algorithm
This calculates P(X|Theta)
"""      
def backward(model, emissions):
    b = util.Counter()
    #minor initialization nuance
    for state in model.getStates() : b[state] = 1
    emissions.reverse()
    for q in emissions[:len(emissions)-1]:
        b_prev = util.Counter()
        for state_k in model.getStates():
            b_prev[state_k] = sum([model.a(state_k, state_l)*model.e(state_l, q)*b[state_l] for state_l in model.getStates()])
        b = b_prev.copy()
    for state in model.getStates():
        b[state] = model.p(state)*model.e(state, emissions[len(emissions)-1])*b[state]
    return b.totalCount()

"""
backward_log:
The same thing as backward, but returns log values
"""
def backward_log(model, emissions):
    B = util.Counter()
    #minor initialization nuance
    for state in model.getStates() : B[state] = math.log(1)
    emissions.reverse()
    for q in emissions[:len(emissions)-1]:
        B_prev = util.Counter()
        for state_k in model.getStates():
            B_prev[state_k] = logSum([model.a_log(state_k, state_l) + model.e_log(state_l, q) + B[state_l] for state_l in model.getStates()])
        B = B_prev.copy()
    for state in model.getStates():
        B[state] = model.p_log(state) + model.e_log(state, emissions[len(emissions)-1]) + B[state]
    return logSum(B.values())
    
"""
Analogous to getForwardList:
For the baum-welch algorithm we need b_l(t)
for every state l and for every t in len(emission)
instead of recalculating the same previous values
again we're just gonna store them sequentially
in a list of dictionaries

Note: we have to return the reversed list because
we iterate backwards and in order for the list index, i 
to match t we must reverse the list
"""

def getBackwardList(model, emissions1):
    emissions = emissions1[:]
    b = util.Counter()
    #minor initialization nuance
    for state in model.getStates() : b[state] = 1
    emissions.reverse()
    backwardList = []
    for q in emissions[:len(emissions)-1]:
        b_prev = util.Counter()
        for state_k in model.getStates():
            b_prev[state_k] = sum([model.a(state_k, state_l)*model.e(state_l, q)*b[state_l] for state_l in model.getStates()])
        b = b_prev.copy()
        backwardList.append(b)
    b_last = util.Counter()
    for state in model.getStates():
        b_last[state] = model.p(state)*model.e(state, emissions[len(emissions)-1])*b[state]
    backwardList.append(b_last)
    backwardList.reverse()
    return backwardList

    
"""
getBackwardList_log
The same thing as getBackwardList, but returns log values
"""
def getBackwardList_log(model, emissions):
    B = util.Counter()
    #minor initialization nuance
    for state in model.getStates() : B[state] = math.log(1)
    emissions.reverse()
    backwardList_log = []
    backwardList_log.append(B)
    for q in emissions[:len(emissions)-1]:
        B_prev = util.Counter()
        for state_k in model.getStates():
            B_prev[state_k] = logSum([model.a_log(state_k, state_l) + model.e_log(state_l, q) + B[state_l] for state_l in model.getStates()])
        B = B_prev.copy()
        backwardList_log.append(B)
    B_last = util.Counter()
    for state in model.getStates():
        B_last[state] = model.p_log(state) + model.e_log(state, emissions[len(emissions)-1]) + B[state]
    backwardList_log.reverse()
    return backwardList_log

#######################################################################################
"""
The Baum-Welch Algorithm

The model is improved until the difference
between the log likelihood of the current model
previous model are under the threshold
"""


"""
baum_welch_log
this is the baum_welch algorithm running in log-space

INPUT: HMM model, (list) of training sequences, (int) the number of times to run
OUTPUT: new HMM model based on new estimated parameters
"""
def baum_welch_log(model, sequences, numRuns):
    for n in range(numRuns):
        print "[baum_welch_log algo] BW_Iteration #: ", n + 1
        sequenceFBList = []
        for sequence in sequences:
            forwardList = getForwardList_log(model, sequence[:])
            forwardLog = logSum([forwardList[len(forwardList)-1][state] for state in model.getStates()])
            backwardList = getBackwardList_log(model, sequence[:])
            sequenceFBList.append((forwardList, forwardLog, backwardList))
        #E-Step: Calculating the expected Transisions (A)
        expectedTransitions = util.Counter()
        print "[baum_welch_log algo] calculating transistions, please wait"
        for k,l in [(k,l) for k in model.getStates() for l in model.getStates()]:
            seqListA = []
            for i in range(len(sequences)):
                sequence = sequences[i]
                forwardList = sequenceFBList[i][0]
                forwardLog = sequenceFBList[i][1]
                backwardList = sequenceFBList[i][2]
                sumListA = []
                for i in range(len(sequence)-1):
                    sumListA.append(forwardList[i][k] + model.a_log(k,l) + model.e_log(l, sequence[i+1]) + backwardList[i+1][l])
                if len(sumListA) == 0:
                    print "Error: Transition Probability of 0 for Baum-Welch working in log-space"
                    return
                seqListA.append(logSum(sumListA) - forwardLog)
            if len(seqListA) == 0:
                print "Error: Transition Probability of 0 for Baum-Welch working in log-space"
                return
            expectedTransitions[(k,l)] = logSum(seqListA)
        #E-Step: Calculating the expected emissions (E)
        expectedEmissions = util.Counter()
        print "[baum_welch_log algo] calculating emissions, please wait"
        for k,b in [(k,b) for k in model.getStates() for b in model.getEmissions()]:
            seqListB = []
            for i in range(len(sequences)):
                sequence = sequences[i]
                forwardList = sequenceFBList[i][0]
                forwardLog = sequenceFBList[i][1]
                backwardList = sequenceFBList[i][2]
                sumListB = []
                for i in range(len(sequence)):
                    if sequence[i] == b:
                        sumListB.append(forwardList[i][k] + backwardList[i][k])
                if len(sumListB) == 0:
                    print "Error: Transition Probability of 0 for Baum-Welch working in log-space"
                    return
                seqListB.append(logSum(sumListB) - forwardLog)
            if len(seqListB) == 0:
                print "Error: Transition Probability of 0 for Baum-Welch working in log-space"
                return
            expectedEmissions[(k,b)] = logSum(seqListB)
        #M-Step
        print "[baum_welch_log algo] Within the M-Step, please wait"
        new_a = {}
        for k,l in [(k,l) for k in model.getStates() for l in model.getStates()]:
            new_a[(k,l)] = expectedTransitions[(k,l)] - logSum([expectedTransitions[(k,l_2)] for l_2 in model.getStates()])
        new_e = {}
        for k,b in [(k,b) for k in model.getStates() for b in model.getEmissions()]:
            new_e[(k,b)] = expectedEmissions[(k,b)] - logSum([expectedEmissions[(k,b_2)] for b_2 in model.getEmissions()])
        model = hmm.HMM(True, model.getStates(), model.getEmissions(), new_a, new_e, model.getMarginal_log())
    return model

#######################################################################################
"""
decodings (viterbi, posterior, posterior mean)
INPUT: HMM model, (list) of emissions
OUTPUT: (list) of 3-tuple: (viterbi, posterior, posterior mean)
"""

def decodings(model, emissions):
    stateMapper = {1:0.32, 2:1.75, 3:4.54, 4:9.40}
    V = util.Counter()
    ptr = util.Counter()
    forwardList = getForwardList_log(model, emissions[:])
    backwardList = getBackwardList_log(model, emissions[:])
    logLikelihood = logSum([forwardList[len(forwardList)-1][state] for state in model.getStates()])
    for state in model.getStates():
        V[state] = model.p_log(state) + model.e_log(state, emissions[0])
    pointers = []
    emissionsOld = emissions[:]
    emissions = emissions[1:]
    for t in range(len(emissions)):
        V_next = util.Counter()
        ptr = util.Counter()
        for state_l in model.getStates():
        
            maxCounter = util.Counter()
            for state in model.getStates():
                maxCounter[state] = model.a_log(state, state_l) + V[state]
            ptr[state_l] = maxCounter.argMax()
            
            V_next[state_l] = model.e_log(state_l, emissions[t]) + max([model.a_log(state_k, state_l) + V[state_k] for state_k in model.getStates()])
        pointers.append(ptr)
        V = V_next.copy()
    lastState = V.argMax()
    values = [lastState]
    posterior = []
    for i in range(len(emissionsOld)):
        counterOfStates = util.Counter()
        for s in model.getStates():
            counterOfStates[(i,s)] = (forwardList[i][s] + backwardList[i][s]) - logLikelihood
        mean = sum([stateMapper[state]*math.exp(counterOfStates[(i,state)]) for state in model.getStates()])
        posterior.append((counterOfStates.argMax()[1], mean))
    pointers.reverse()
    for i in range(len(pointers)):
        lastState = pointers[i][lastState]
        values.append(lastState)
    values.reverse()
    finalValues = [(values[i],posterior[i][0], posterior[i][1]) for i in range(len(posterior))]    
    return finalValues
