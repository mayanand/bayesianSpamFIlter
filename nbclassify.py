#!/usr/bin/env python

import sys, pprint, functools, os, glob
from math import log

class nbclassify(object):
    """
        class to classiy mails based on nbmodel.txt produced by
         nblearn.py
    """
    def __init__(self):
        self.nbmod_dict = {}

    def classify(self, file, outputHandle):

        words = []
        with open(file, "r", encoding="latin1") as f:
            words = f.read().split()

        wordSpam = []
        for x in words:
            if x in self.nbmod_dict['word']:
                wordSpam.append(self.nbmod_dict['word'][x][0])

        logSpam = list(map(log, wordSpam))
        spamProb = functools.reduce(lambda x, y: x + y, logSpam) + log(self.nbmod_dict['spam'])

        wordHam = []
        for x in words:
            if x in self.nbmod_dict['word']:
                wordHam.append(self.nbmod_dict['word'][x][1])

        logHam = list(map(log, wordHam))
        hamProb = functools.reduce(lambda x, y: x + y, logHam) + log(self.nbmod_dict['ham'])

        if hamProb > spamProb:
            outputHandle.write(str("HAM " + file + "\n"))
        else:
            outputHandle.write(str("SPAM " + file + "\n"))

        return


if __name__ == "__main__":
    if (len(sys.argv)) != 2:
        print("Usage: python3 nblearn.py /path/to/input")
        exit(1)

    dataPath = sys.argv[1]

    print("The file name is: ", dataPath)
    print("Somet")

    nbmodel = {}

    with open("nbmodel.txt",'r') as f:
        nbmodel = eval(f.read())

    # pprint.pprint(nbmodel)

    nbclassify_obj = nbclassify()
    nbclassify_obj.nbmod_dict = nbmodel

    devFiles = []

    for root, dirnames, filenames in os.walk(dataPath):
        for file in filenames:
            if file.endswith(".txt"):
                devFiles.append(os.path.join(root, file))

    try:
        outputHandle = open('nboutput.txt', 'w')
    except:
        print("issue with file io")

    for file in devFiles:
        nbclassify_obj.classify(file, outputHandle)


    outputHandle.close()

    print("Done with everything")

    # learn_obj = Learn()
    # learn_obj.fname = dataPath
    # learn_obj.getData()
    # learn_obj.find_token_probability()


