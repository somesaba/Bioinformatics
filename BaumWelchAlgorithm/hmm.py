# hmm.py
# ----------
# HMM_TMRCA Project
# Licensing Information: Please do not distribute.
# You are free to use and extend these code for educational purposes.
# ProblemSet written by professor Yun S. Song
# Solution and code written by Jae Young Ryoo (jay.ryoo@gmail.com) and Saba Khalilnaji

import sys, math

"""
HMM Class
holds both logarithmic and non-logarithmic parameter values as well as
states and emission sets
"""

class HMM:
    
    def a(self,k,l):
        if self.isAHiddenState(k) and self.isAHiddenState(l):
            return self.transitionProbabilities[(k,l)]
        else:
            print "ERROR: k=%s or l=%s not a hidden state" % (k,l)
            return
        
    def a_log(self,k,l):
        if self.isAHiddenState(k) and self.isAHiddenState(l):
            return self.transitionProbabilities_log[(k,l)]
        else:
            print "ERROR: k=%s or l=%s not a hidden state" % (k,l)
            return
        
    def e(self,k,b):
        if not self.isAnEmission(b):
            print "ERROR: b=%s is not an emission" % b
            return
        if not self.isAHiddenState(k):
            print "ERROR k=%s is not a hidden state" % k
            return
        return self.emissionProbabilities[(k,b)]
    
    def e_log(self,k,b):
        if not self.isAnEmission(b):
            print "ERROR: b=%s is not an emission" % b
            return
        if not self.isAHiddenState(k):
            print "ERROR k=%s is not a hidden state" % k
            return
        return self.emissionProbabilities_log[(k,b)]
        
    def p(self, k):
        if not self.isAHiddenState(k):
            print "ERROR k=%s is not a hidden state" % k
            return
        return self.marginal[k]

    def p_log(self, k):
        if not self.isAHiddenState(k):
            print "ERROR k=%s is not a hidden state" % k
            return
        return self.marginal_log[k]
        
    def getMarginal(self):
        return self.marginal

    def getMarginal_log(self):
        return self.marginal_log
        
    def getStates(self):
        return self.stateSpace
    
    def getEmissions(self):
        return self.emissions

    def getTransitionProbabilities(self):
        return self.transitionProbabilities

    def getTransitionProbabilities_log(self):
        return self.transitionProbabilities_log

    def getEmissionProbabilities(self):
        return self.emissionProbabilities

    def getEmissionProbabilities_log(self):
        return self.emissionProbabilities_log
        
    #############################################
    #             Helper methods:               #          
    # You shouldn't need to call these directly #
    #############################################
    """
    bool_log is a boolean that is true if parameters are log, false if normal values
    s is a list of hidden states
    q is a list of emission states
    a is a dictionary of transition probailities k to l with (k,l) as keys
    e is a dictionary of emission probabilities b from k with (k, b) as the keys
    marginal is the marginal probability that Q_1 = k, this is a dictionary with 
        k as the key
    """
    def __init__(self,bool_log, s, q, a, e, marginal):
        self.stateSpace = s
        self.emissions = q
        if bool_log:
            self.transitionProbabilities_log = a
            self.emissionProbabilities_log = e
            self.marginal_log = marginal
            self.transitionProbabilities = self.makeExp(a)
            self.emissionProbabilities = self.makeExp(e)
            self.marginal = self.makeExp(marginal)
        else:
            self.transitionProbabilities = a
            self.transitionProbabilities_log = self.makeLog(a)
            self.emissionProbabilities = e
            self.emissionProbabilities_log = self.makeLog(e)
            self.marginal = marginal
            self.marginal_log = self.makeLog(marginal)

    def makeLog(self, param):
        newParam = {}
        for k, v in param.iteritems():
            newParam[k] = math.log(float(v))
        return newParam
    
    def makeExp(self, param):
        newParam = {}
        for k, v in param.iteritems():
            newParam[k] = math.exp(float(v))
        return newParam
        
    def isAHiddenState(self, s):
        return s in self.stateSpace
        
    def isAnEmission(self, q):
        return q in self.emissions
        
    def __str__(self):
        s = "Hidden States:\n" + str(self.stateSpace) + "\n"
        s += "Emission States:\n" + str(self.emissions) + "\n"
        s += "Tranistion Probabilities:\n" + str(self.transitionProbabilities) + "\n"
        s += "Emission Probabilities:\n" + str(self.emissionProbabilities) + "\n"
        s += "Marginals:\n" + str(self.marginal)
        return s
    
