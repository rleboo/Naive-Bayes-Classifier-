"""evaluate.py used to leave one out valuation for data passed to naivebayes.py"""

import sys
import os

def main():

    fileName = open(sys.argv[1], 'r')

    lines = [line.rstrip('\n') for line in fileName]

    pastPart = False

    #Stores sample data
    samples = []
    sampleCopy = []

    preamble = ""
    #Obtains all sample data. Adds preamble to training/validation file


    #List of all the classes
    classList = []
    for item in lines:
        if pastPart:
            item.strip()
            samples.append(item)
            sampleCopy.append(item)
        else:
            preamble = preamble + item + '\n'

        if "@data" in item:
            pastPart = True
        if "@attribute" in item:
            key = item[item.find("{") + 1:item.find("}")]
            att = [x.strip() for x in key.split(',')]
            classList.append(att)

    classList = classList.pop(len(classList)-1)
    cla = {}
    arrayList = []
    #Class Index isn't used further
    for x in range(len(classList)):
        cla[classList[x]] = x
        arrayList.append(classList[x])


    correctAnswers = []

    sampleTemp = samples
    loopLength = len(sampleTemp)

    tracker = 0
    for i in range(loopLength):
        valItem = samples[i]
        correctAnswers.append(valItem.split(',')[-1])

        fileN = "validation.txt"
        fileName = open(fileN, 'w')

        fileName.write(preamble + valItem + '\n')
        trainList = ""

        #Obtain list of true classes

        for item in samples:
            if item != samples[i]:
                trainList += item + '\n'

        train = "training.txt"
        trainName = open(train, 'w')
        trainName.write(preamble + trainList + '\n')
        trainName.close()
        fileName.close()
        #Change to python3
        os.system('python3 naivebayes.py training.txt validation.txt result.txt')
        tracker += 1
        print("Training/Validation Set. #: " + str(tracker))

    #Confusion Matrix
    #Need to get a list of inputs. This is in Correct Answer

    calFile = open('result.txt', 'r')

    lin = [line.rstrip('\n') for line in calFile]

    calculatedAnswer = []
    for lop in lin:
        ans = lop.split()
        calculatedAnswer.append(ans[0])

    calFile.close()

    correct = 0
    for x in range(len(correctAnswers)):
        if correctAnswers[x] == calculatedAnswer[x]:
            correct += 1


    overallAccuracy = correct/len(correctAnswers)

    doubleArray = [[0] * len(cla) for _ in range(len(cla))]
    for i in range(len(correctAnswers)):

        doubleArray[cla[correctAnswers[i]]][cla[calculatedAnswer[i]]] += 1

    firstLie = ""
    for it in cla.keys():
        firstLie += it + "\t"
    confusion = open('confusionMatrix.txt', 'w')
    confusion.write('\t' + firstLie + '\n')

    for i in range(len(doubleArray)):
        add = ""
        add += arrayList[i] + "\t"
        for itm in doubleArray[i]:
            add += str(itm) + "\t"
        confusion.write(add + '\n')

    confusion.write('\n')
    confusion.write("Overall Accuracy: " + str(overallAccuracy))
    #Get predicted outcomes from training list

main()
