# parser.py
# ----------
# HMM_TMRCA Project
# Licensing Information: Please do not distribute.
# You are free to use and extend these code for educational purposes.
# ProblemSet written by professor Yun S. Song
# Solution and code written by Jae Young Ryoo (jay.ryoo@gmail.com) and Saba Khalilnaji

import sys, math, util, hmm

"""
pparser takes in a textFile and parses an initial_parameters.txt file
according to the example set in README
"""
class pparser:
    def __init__(self):
        self.p = {}
        self.e = {}
        self.a = {}
    #def parse_States(self, textFile):
        
    def parse_Parameters(self, textFile):
        pFile = open(textFile)
        i = 0
        l = pFile.next()
        try:
            while True:
                if i == 0:
                    if l[0] == '#':
                        l = pFile.next()
                        continue
                    elif l == '\n':
                        l = pFile.next()
                        l = pFile.next()
                        i = i+1
                        continue
                    else:
                        while l != '\n':
                            l = l.lstrip(' ')
                            l = l.rstrip(' ')
                            trip = l.partition(" ")
                            k = int(trip[0])
                            trip = trip[2].lstrip()
                            trip = trip.rstrip()
                            prob = float(trip)
                            self.p[k] = prob
                            l = pFile.next()
                elif i == 1:
                    if l[0] == '#':
                        l = pFile.next()
                        continue
                    elif l == '\n':
                        l = pFile.next()
                        l = pFile.next()
                        i = i + 1
                        continue
                    else:
                        t = 1
                        while l != '\n':
                            l = l.lstrip()
                            l = l.rstrip()
                            trip = l.partition("	")
                            one = float(trip[0])
                            trip = trip[2].lstrip()
                            trip = trip.partition("	")
                            two = float(trip[0])
                            trip = trip[2].lstrip()
                            trip = trip.partition("	")
                            three = float(trip[0])
                            trip = trip[2].lstrip()
                            trip = trip.partition("	")
                            four = float(trip[0])
                            self.a[(t,1)] = one
                            self.a[(t,2)] = two
                            self.a[(t,3)] = three
                            self.a[(t,4)] = four
                            t = t + 1
                            l = pFile.next()
                elif i == 2:
                    if l[0] == '#':
                        l = pFile.next()
                        continue
                    else:
                        while l != '\n':
                            l = l.lstrip()
                            l = l.rstrip()
                            trip = l.partition(" ")
                            kk = int(trip[0])
                            trip = trip[2].lstrip()
                            trip = trip.partition(" ")
                            II = float(trip[0])
                            trip = trip[2].lstrip()
                            DD = float(trip)
                            self.e[(kk, 'D')] = DD
                            self.e[(kk, 'I')] = II
                            l = pFile.next()
        except:
            pass
        pFile.close()
        return(self.p, self.a, self.e)
