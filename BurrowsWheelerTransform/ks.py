import sys, types, time, random, os, math
import util

def cd3(T):
    #The KS Algorithm

    ########Step 0: construct a sample#######
    n = len(T)
    base1 = max(T) + 1
    base2 = max((max(T) + 1), n + 1)
    B0 = []
    B1 = []
    B2 = []
    Bk = {0: B0, 1: B1, 2: B2}

    #B1 and B2 contain indicies that are mod3 = 1, mod3 = 2, respectively
    for i in xrange(n+1):
        Bk[i % 3] += [i]

    # C is the concatenation of B1 and B2
    C = B1 + B2

    #######Step 1: Sort Sample Suffixes#######
    #we assume that t_j = 0 for j >= n but since we dont go above j = 3 adding 5 is safe
    T += [0,0,0,0,0]

    #constructing Strings with suffixes as characters
    #R_k = [t_k,t_k+1,t_k+2][t_k+3,t_k+4,t_k+5]...[t_maxBk,t_maxBk+1,t_maxBk+2]
    #R = R1 concatenated with R2
    R1 = []
    R2 = []

    #Here we add a new varable to our tuple. Our sets of three characters (t_k,t_k+1,t_k+2) will be
    #((t_k,t_k+1,t_k+2), i) where i represents the suffix this triple represents in our original string
    for i in B1:
        R1 += [((T[i], T[i+1], T[i+2]),i)]
    for i in B2:
        R2 += [((T[i], T[i+1], T[i+2]),i)]
    R = R1 + R2

    #Because dealing with this modifided data structure is difficult, we also create one without the
    #index 
    #R_sorted is R with indicies sorted lexicographically
    #R_sorted_woIndex is R_woIndex sorted lexicographically
    R_woIndex = [char[0] for char in R]
    R_sorted = util.radixSort(list(set(R)), base1, 3, True)
    R_sorted_woIndex = util.radixSort(list(set(R_woIndex)), base1, 3, False)

    #R_prime gives us the string R with characters replaced by their ranking
    #SA_R_Prime = suffix array of R prime
    R_prime = util.renameWithRank(R_woIndex, R_sorted_woIndex)
    SA_R_Prime = []
    rank = {}

    #If there are duplicates we need to recurse and change the sorting of R
    if len(R_prime) != len(set(R_prime)):
        SA_R_Prime = cd3(R_prime)
        SA_R_Prime.pop(0)
        
        #if there are duplicates we change how we calculate rank with given data structures
        #Because the suffix array gives us suffix positions of R in lexicographic order,
        #we look up the R value and use the index of T to match up with the ranking of a
        #suffix of R
        for i in range(len(SA_R_Prime)):
            rank[R[SA_R_Prime[i]][1]] = i+1
        rank[n+1] = 0
        rank[n+2] = 0
        
        #This also means we change R_sorted based on the suffix array now
        R_sorted = [R[SA_R_Prime[i]] for i in range(len(SA_R_Prime))]
        
    #otherwise we just match up the rankings by matching R_prime values to indices of T
    #and since both are in corresponding order we just match them up
    else:
        for i in range(len(C)):
            rank[C[i]] = R_prime[i]
        rank[n+1] = 0
        rank[n+2] = 0

    #######Step2: Sort Nonsample Suffixes#######
    #here we need to sort nonsample suffixes
    #nsSuffixes = nonsample suffixes
    nsSuffixes = []
    for i in B0:
        nsSuffixes.append(((T[i],rank[i+1]), i))
    nsSuffixes_sorted = util.radixSort(nsSuffixes, base2, 2, True)

    #######Step3: Merge#######
    #splSuffix_sorted = sample suffix indices in sorted order
    #nsplSuffix_sorted = non sample suffix indices in sorted order
    splSuffix_sorted = [num[1] for num in R_sorted]
    nsplSuffix_sorted = [num[1] for num in nsSuffixes_sorted]
    suffixArray = []

    # a simple comparison based merge
    for i in range(n+1):
        if len(splSuffix_sorted) <= 0:
            suffixArray += nsplSuffix_sorted
            break
        if len(nsplSuffix_sorted) <= 0:
            suffixArray += splSuffix_sorted
            break
        spI = splSuffix_sorted[0]
        spJ = nsplSuffix_sorted[0]
        if spI%3 == 1:
            if (T[spI], rank[spI+1]) <= (T[spJ], rank[spJ+1]):
                suffixArray.append(splSuffix_sorted.pop(0))
            else:
                suffixArray.append(nsplSuffix_sorted.pop(0))
        if spI%3 == 2:
            if (T[spI], T[spI+1], rank[spI+2]) < (T[spJ], T[spJ+1], rank[spJ+2]):
                suffixArray.append(splSuffix_sorted.pop(0))
            else:
                suffixArray.append(nsplSuffix_sorted.pop(0))
    #print "suffixArray: ", suffixArray
    #print "len sA: ", len(suffixArray)
    return suffixArray

    
    

        

