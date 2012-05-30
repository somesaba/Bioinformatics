import sys, types, time, random, os
import radix
from math import log

#Simple functions that help out with the KS Algorithm

#Converting to a numerical Alphabet occurs when
#the String is initially given to the program

def convertToNumAlphabet(T):
    T_ascii = [ord(char) for char in T]                 #the string T in ascii values
    Tascii_minRepeats = list(set(T_ascii))              #the string T in ascii values minus repeats
    T_Radixed = radix.radixSort(Tascii_minRepeats, 10)  #radixed string T in ascii values                                       
    dic = {}
    for i in range(1,len(T_Radixed)+1):
        dic[T_Radixed[i-1]] = i
    return [dic[num] for num in T_ascii]
    
def convertToNumAlphabet2(T):
    T_ascii = [ord(char) for char in T]                 #the string T in ascii values
    Tascii_minRepeats = list(set(T_ascii))              #the string T in ascii values minus repeats
    T_Radixed = radix.radixSort(Tascii_minRepeats, 10)  #radixed string T in ascii values                                       
    dic = {}
    for i in range(1,len(T_Radixed)+1):
        dic[T_Radixed[i-1]] = i
    newVals = [chr(k) for k in dic.keys()]
    new_dict = dict(zip(dic.values(),newVals))
    return ([dic[num] for num in T_ascii], new_dict)
    
def convertToString(T, dic):
    return [dic[n] for n in T]
    

# renaming R with rank
def renameWithRank(R, R_sorted):
    R_output = []
    dic = {}
    for i in range(1,len(R_sorted)+1):
        dic[R_sorted[i-1]] = i
    for i in range(len(R)):
        R_output.append(dic[R[i]])
    return R_output

#RADIX for tuples
def getDigit(num, digit_num, indexed):
    # pulls the selected digit
    if indexed:
        return num[0][digit_num]
    else:
        return num[digit_num]
 
def makeBlanks(size):
    # create a list of empty lists to hold the split by digit
    return [ [] for i in range(size) ]  
 
def split(a_list, base, digit_num, indexed):
    buckets = makeBlanks(base)
    for num in a_list:
        # append the number to the list selected by the digit
        buckets[getDigit(num, digit_num, indexed)].append(num)  
    return buckets
 
# concatenate the lists back in order for the next step
def merge(a_list): 
    new_list = []
    for sublist in a_list:
       new_list.extend(sublist)
    return new_list
 
def radixSort(a_list, base, passes, indexed):
    # there are as many passes as there are digits in the longest number
    #indexed indicates whether or not an indicy is present
    new_list = list(a_list)
    for digit_num in range(passes-1,-1,-1):
        new_list = merge(split(new_list, base, digit_num, indexed))
    return new_list

class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.

    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.  Using a dictionary:

    a = {}
    print a['test']

    would give an error, while the Counter class analogue:

    >>> a = Counter()
    >>> print a['test']
    0

    returns the default 0 value. Note that to reference a key
    that you know is contained in the counter,
    you can still use the dictionary syntax:

    >>> a = Counter()
    >>> a['test'] = 2
    >>> print a['test']
    2

    This is very useful for counting things without initializing their counts,
    see for example:

    >>> a['blah'] += 1
    >>> print a['blah']
    1

    The counter also includes additional functionality useful in implementing
    the classifiers for this assignment.  Two counters can be added,
    subtracted or multiplied together.  See below for details.  They can
    also be normalized and their total count and arg max can be extracted.
    """
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        """
        Increments all elements of keys by the same count.

        >>> a = Counter()
        >>> a.incrementAll(['one','two', 'three'], 1)
        >>> a['one']
        1
        >>> a['two']
        1
        """
        for key in keys:
            self[key] += count

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        """
        Returns a list of keys sorted by their values.  Keys
        with the highest values will appear first.

        >>> a = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> a['third'] = 1
        >>> a.sortedKeys()
        ['second', 'third', 'first']
        """
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def __mul__(self, y ):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['second'] = 5
        >>> a['third'] = 1.5
        >>> a['fourth'] = 2.5
        >>> a * b
        14
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> a += b
        >>> a['first']
        1
        """
        for key, value in y.items():
            self[key] += value

    def __add__( self, y ):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a + b)['first']
        1
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__( self, y ):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a - b)['first']
        -5
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend

