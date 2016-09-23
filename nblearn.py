#!/usr/bin/env python
import os, sys, glob
from collections import defaultdict
from collections import Counter

class Learn(object):
    def __init__(self):
        self.fname = ""
        self.vocabList  = []
        self.spamTrainingCount = 0  #contains total spam training data
        self.hamTrainingCount = 0   #contans total ham training data
        self.totalTrainingCount = 0
        self.spamWordCount = {}
        self.hamWordCount = {}
        self.spamFiles = []
        self.hamFiles = []
        self.spamWordList = []
        self.hamWordList = []
        self.proDict = {'word' : {},
                        'spam' : 0,
                        'ham': 0
                        }
        
        
    def getData(self):
        """
            This function is used to parse the vocab list and training data provided to us.
        """


        print("inside getdaat")

        for root, dirnames, filenames in os.walk(self.fname):
            if "spam" in dirnames:
                spamdir = os.path.join(root, "spam")
                self.spamFiles.extend([os.path.join(spamdir, x) for x in os.listdir(spamdir) if x.endswith(".txt")])

        for sFile in self.spamFiles:
            with open(sFile, "r", encoding="latin1") as f:
                self.spamWordList.extend(f.read().split())

        self.vocabList.extend(self.spamWordList)

        for root, dirnames, filenames in os.walk(self.fname):
            if "ham" in dirnames:
                hamdir = os.path.join(root, "ham")
                self.hamFiles.extend([os.path.join(hamdir, x) for x in os.listdir(hamdir) if x.endswith(".txt")])


        for hFile in self.hamFiles:
            with open (hFile, "r", encoding="latin1") as f:
                self.hamWordList.extend(f.read().split())

        self.vocabList.extend(self.hamWordList)

        self.vocabList = list(set(self.vocabList))

        #print(len(self.spamWordList))
        # print len(self.spamWordList)
        
        return
        
    def find_token_probability(self):

        print("inside token probability")

        print("vocab list")
        print(len(self.vocabList))
        # exit(1)


        self.spamWordCount = Counter(self.spamWordList)

        # print("getting spam word count")



        self.hamWordCount = Counter(self.hamWordList)


        self.spamTrainingCount = len(self.spamFiles)
        self.hamTrainingCount = len(self.hamFiles)
        
        # print self.spamTrainingCount
        # print self.hamTrainingCount
        self.totalTrainingCount = self.spamTrainingCount + self.hamTrainingCount

        self.proDict = {'word': {},
                        'spam': 0,
                        'ham': 0
                        }

        distinctWordLen = len(self.vocabList)
        for word in self.vocabList:
            self.proDict['word'][word] = (((self.spamWordCount[word] + 1) / (len(self.spamWordList) + distinctWordLen))  , \
                                          ((self.hamWordCount[word] + 1)/ (len(self.hamWordList) + distinctWordLen)))

        self.proDict['spam'] = self.spamTrainingCount / self.totalTrainingCount
        self.proDict['ham'] = self.hamTrainingCount / self.totalTrainingCount

        # print("******** reached this place")


        try:
            with open('nbmodel.txt', 'w') as f:
                print("opened the file and writing to it")
                f.write(str(self.proDict))
        except:
            print("something went wrong with FIL IO")
            exit(1)

        # print self.spamWordCount
        # print self.hamWordCount
        # print self.wordSpamProbDict    
        return
    
if __name__ == "__main__":
    if (len(sys.argv)) != 2:
        print("Usage: python3 nblearn.py /path/to/input")
        exit(1)

    dataPath = sys.argv[1]

    print("The file name is: ", dataPath)

    learn_obj = Learn()
    learn_obj.fname = dataPath
    learn_obj.getData()
    learn_obj.find_token_probability()
