import sys, math

def outputToFile(outputFile, outputList, bType, inputFileReadLine):
    outputFile.write('>'+ bType + ': ' + inputFileReadLine)
    tempLine = ""
    for i in range(len(outputList)):
        if i%80 == 0:
            outputFile.write(tempLine + '\n')
            tempLine = outputList[i]
        else:
            tempLine += outputList[i]
    outputFile.write(tempLine + '\n')
    
def inputToList(inputFile):
    S = ""
    for line in inputFile:
        S += line.strip()
    S = list(S)
    if S[len(S)-1] == '$':
        S.pop()
    return S
    
