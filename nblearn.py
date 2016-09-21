#!/usr/bin/env python
# from __future__ import division
import os, sys, glob, pprint
from collections import defaultdict
from collections import Counter

class Learn(object):
    def __init__(self):
        self.fname = ""
        #self.currentDir = os.getcwd()
        self.vocabList  = []
        self.tokenCount = {}    #contains the word count in spam and ham in total
        self.spamTrainingCount = 0  #contains total spam training data
        self.hamTrainingCount = 0   #contans total ham training data
        self.totalTrainingCount = 0
        self.spamWordCount = defaultdict(lambda: 1)
        self.hamWordCount = defaultdict(lambda: 1)
        self.tokenProbability = defaultdict(lambda: 1)  #contains the probability of every token n spam and ham
        self.spamFiles = []
        self.hamFiles = []
        self.spamProbability = 0.5  #taking unbiased probabiity of spam
        self.hamProbability = 0.5   #taking ubiased probability of ham
        self.spamWordList = []
        self.hamWordList = []
        self.proDict = {'word' : {},
                        'spam' : 0,
                        'ham': 0
                        }
        self.wordSpamProbDict = {}      #probability of every word in a spam mail
        self.wordHamProbDict= {}        #pribablity of every word in a ham mail
        
        
    def getData(self):
        """
            This function is used to parse the vocab list and training data provided to us.
        """
        # self.vocabList = [line.rstrip('\n') for line in open(self.fname)]


        print("inside getdaat")


        spamFolder = os.path.join(self.fname, "train\*\spam\*.txt")
        self.spamFiles = [name for name in glob.glob(spamFolder)]
        #print(spamFiles)


        for sFile in self.spamFiles:
            with open(sFile, "r", encoding="latin1") as f:
                self.spamWordList.extend(list(f.read().split()))

        self.vocabList.extend(self.spamWordList)

        hamFolder = os.path.join(self.fname, "train\*\ham\*.txt")
        self.hamFiles = [name for name in glob.glob(hamFolder)]
        #print(spamFiles)

        for hFile in self.hamFiles:
            with open (hFile, "r", encoding="latin1") as f:
                self.hamWordList.extend(list(f.read().split()))

        self.vocabList.extend(self.hamWordList)

        self.vocabList = list(set(self.vocabList))

        #print(len(self.spamWordList))

        # print len(self.spamWordList)
        # print self.spamWordList.count("viagra")        
        # print self.hamWordList
        # print len(self.hamWordList)
        # print self.hamWordList.count("viagra")
        
        return
        
    def find_token_probability(self):

        print("inside token probability")

        print("vocab list")
        print(len(self.vocabList))
        # exit(1)


        self.spamWordCount = Counter(self.spamWordList)

        print("getting spam word count")



        self.hamWordCount = Counter(self.hamWordList)
        # for word in self.vocabList:
        #     print("ust entered for loop")
        #     self.spamWordCount[word] = self.spamWordList.count(word)
        #     print("counter spam")
        #     self.hamWordCount[word] = self.hamWordList.count(word)

        print("after for loop")

        self.spamTrainingCount = len(self.spamFiles)
        self.hamTrainingCount = len(self.hamFiles)
        
        # print self.spamTrainingCount
        # print self.hamTrainingCount
        self.totalTrainingCount = self.spamTrainingCount + self.hamTrainingCount

        self.proDict = {'word': {},
                        'spam': 0,
                        'ham': 0
                        }

        for word in self.vocabList:
            self.proDict['word'][word] = [(self.spamWordCount[word] + 1 / self.spamTrainingCount) , \
                                          (self.hamWordCount[word] + 1/ self.hamTrainingCount)]

        self.proDict['spam'] = self.spamTrainingCount / self.totalTrainingCount
        self.proDict['ham'] = self.hamTrainingCount / self.totalTrainingCount

        print("******** reached this place")


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
    print("Somet")

    learn_obj = Learn()
    learn_obj.fname = dataPath
    learn_obj.getData()
    learn_obj.find_token_probability()
