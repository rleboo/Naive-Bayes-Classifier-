"""naivebayes.py uses the naive bayes theorem to classify different clases from their given features"""
import sys


def training():
    return "dog"



def main():

    #fileName = open('sampletraining.arff', 'r')
    fileName = open(sys.argv[1], 'r')


    lines = [line.rstrip('\n') for line in fileName]

    dic = {}

    #Keeps track of feature names
    anotherList = []

    #Keeps track of each occurrence of a feature by class
    attributes = {}
    listOF = []

    track = 0
    for item in lines:
        track += 1
        if "@attribute" in item:
            atts = item.split()
            anotherList.append(atts[1])
            # The 2nd position in list is the attribute type

            # Takes features of attributes
            key = item[item.find("{") + 1:item.find("}")]
            att = [x.strip() for x in key.split(',')]
            listOF.append(att)

            # Add to dictionary
            attributes[atts[1]] = att

    cla = listOF.pop(len(listOF)-1)

    for key in attributes:
        for x in cla:
            dic[key+x] = []


    classTracker = {}

    #Keep track of total number of samples
    totaltrack = 0

    pastLine = False
    for item in lines:
        # Data itself

        if pastLine and item != "":
            totaltrack = totaltrack + 1
            datalist = item.strip().split(',')
            if datalist[-1] in classTracker:
                classTracker[datalist[-1]] += 1

            if datalist[-1] not in classTracker:
                classTracker[datalist[-1]] = 1


            for i in range(len(datalist) - 1):
                dic[anotherList[i] + datalist[-1]].append(datalist[i])

        if "@data" in item:
            pastLine = True

    fileName.close()

    ##########################################################################################
    # Data has been trained

    file = open(sys.argv[2], 'r')

    outputFile = open(sys.argv[3], 'a')


    scan = [line.rstrip('\n') for line in file]

    truefalse = False
    for line in scan:

        if truefalse:
            # Stores the Conditions
            datal = line.split(',')

            # used to store final Calculations
            # Need to keep track of total
            ret = {}

            for items in cla:

                # Keep tracks of calculation
                if items in classTracker:
                    totalCal = classTracker.get(items)/totaltrack
                else:
                    totalCal = 0

                for i in range(len(datal) - 1):
                    # Get data at attribute+class location
                    arr = dic.get(anotherList[i] + items)
                   # print(anotherList[i] + items + " " + datal[i])

                    #Count total possibilities.
                    tots = arr.count(datal[i])

                   # print("This is number of possible ways: " + str(tots) + " This is the total ways " + str(len(arr)))
                    """ if tots == 0:
                        totalCal = 0
                    else:
                    """
                    totalCal = totalCal * (tots / len(arr))

                ret[items] = totalCal
            realProbabilities = 0
            for key in ret:
                realProbabilities += ret.get(key)

            maxValue = 0
            maxName = ""
            for cal in ret:
                """if realProbabilities == 0:
                    ret[cal] = 0
                else:
                """
                ret[cal] = ret.get(cal)/realProbabilities
                if(ret[cal] > maxValue):
                    maxValue = ret[cal]
                    maxName = cal


            prin = ""
            for i in ret:
                prin += i + " " + str(ret[i]) + " "
            outputFile.write(maxName + "" + "\t" + prin + '\n')

        if "@data" in line:
            truefalse = True


main()