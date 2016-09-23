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
        self.hamTP = 0
        self.hamTN = 0
        self.hamFP = 0
        self.hamFN = 0
        self.spamTP = 0
        self.spamTN = 0
        self.spamFP = 0
        self.spamFN = 0

        self.stopWordList = ["a", "about", "an", "are", "as", "at", "be", "by", "for",
                             "from", "how", "i", "in", "is", "it", "la", "of", "on", "or",
                             "that", "the", "this", "to", "was", "what", "when", "where",
                             "who", "will", "with", "und", "the", "www"]

    def classify(self, file, outputHandle):

        words = []
        with open(file, "r", encoding="latin1") as f:
            words = f.read().split()

        wordSpam = []
        for x in words:
            if x in self.nbmod_dict['word'] and x not in self.stopWordList:
                wordSpam.append(self.nbmod_dict['word'][x][0])

        logSpam = list(map(log, wordSpam))
        spamProb = functools.reduce(lambda x, y: x + y, logSpam) + log(self.nbmod_dict['spam'])

        wordHam = []
        for x in words:
            if x in self.nbmod_dict['word'] and x not in self.stopWordList:
                wordHam.append(self.nbmod_dict['word'][x][1])

        logHam = list(map(log, wordHam))
        hamProb = functools.reduce(lambda x, y: x + y, logHam) + log(self.nbmod_dict['ham'])

        if hamProb > spamProb:
            if 'ham' in file:
                self.hamTP += 1
                self.spamTN += 1
            else:
                self.hamFP += 1
                self.spamFN += 1
            outputHandle.write(str("HAM " + file + "\n"))
        else:
            if 'spam' in file:
                self.spamTP += 1
                self.hamTN += 1
            else:
                self.spamFP += 1
                self.hamFN += 1

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

    spamPrecision = nbclassify_obj.spamTP / (nbclassify_obj.spamTP + nbclassify_obj.spamFP)
    print("spam precision: ", spamPrecision)

    spamRecall = nbclassify_obj.spamTP / (nbclassify_obj.spamTP + nbclassify_obj.spamFN)
    print("spam recall: ", spamRecall)

    spamF1Score = 2 * ((spamPrecision * spamRecall) / (spamPrecision + spamRecall))
    print("spam F1 score: ", spamF1Score)

    hamPrecision = nbclassify_obj.hamTP / (nbclassify_obj.hamTP + nbclassify_obj.hamFP)
    print("sam precision: ", hamPrecision)

    hamRecall = nbclassify_obj.hamTP / (nbclassify_obj.hamTP + nbclassify_obj.hamFN)
    print("ham recall: ", hamRecall)

    hamF1Score = 2 * ((hamPrecision * hamRecall) / (hamPrecision + hamRecall))
    print("ham F1 score: ", hamF1Score)

    print("Exiting classification")
    exit(0)


    # learn_obj = Learn()
    # learn_obj.fname = dataPath
    # learn_obj.getData()
    # learn_obj.find_token_probability()


