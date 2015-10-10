#!/usr/bin/env python
from __future__ import division
import os

class Learn(object):
    def __init__(self):
        self.fname = "/home/mayank/my_app/spamFilter/data/vocab.dat"
        self.currentDir = os.getcwd()
        self.vocabList  = []
        self.tokenCount = {}    #contains the word count in spam and ham in total
        self.spamTrainingCount = 0  #contains total spam training data
        self.hamTrainingCount = 0   #contans total ham training data
        self.totalTrainingCount = 0
        self.spamWordCount = {}
        self.hamWordCount = {}
        self.tokenProbability = {}  #contains the probability of every token n spam and ham
        self.spamProbability = 0.5  #taking unbiased probabiity of spam
        self.hamProbability = 0.5   #taking ubiased probability of ham
        self.spamWordList = []
        self.hamWordList = []
        self.wordSpamProbDict = {}      #probability of every word in a spam mail
        self.wordProbabilityDict= {}    #pribablity of every word in both spam and ha mails 
        
        
    def getData(self):
        """
            This function is used to parse the vocab list and training data provided to us.
        """
        self.vocabList = [line.rstrip('\n') for line in open(self.fname)]
        spamFolder = os.path.join(self.currentDir, "data/test/spam")
        spamFiles = [ f for f in os.listdir(spamFolder)  if os.path.isfile(os.path.join(spamFolder,f))]
        # print spamFiles
        
        for sFile in spamFiles:        
            with open(os.path.join(spamFolder, sFile)) as f:
                self.spamWordList.append(f.read().replace('\r\n', '').lower())
        
        hamFolder = os.path.join(self.currentDir, "data/test/ham")
        hamFiles = [ f for f in os.listdir(hamFolder)  if os.path.isfile(os.path.join(hamFolder,f))]
        
        for hFile in hamFiles:
            with open (os.path.join(hamFolder, hFile), "r") as f:
                self.hamWordList.append(f.read().replace('\r\n', '').lower())
         
        # print len(self.spamWordList)
        # print self.spamWordList.count("viagra")        
        # print self.hamWordList
        # print len(self.hamWordList)
        # print self.hamWordList.count("viagra")
        
        return
        
    def find_token_probability(self):
        for word in self.vocabList:
            counter = 0
            for spam in self.spamWordList:
                if word in spam:
                    counter = counter + 1
            self.spamWordCount[word] = counter
            
            counter = 0
            for ham in self.hamWordList:
                if word in ham:
                    counter = counter + 1
            self.hamWordCount[word] = counter
        
        self.spamTrainingCount = len(self.spamWordList)
        self.hamTrainingCount = len(self.hamWordList)
        
        # print self.spamTrainingCount
        # print self.hamTrainingCount
        self.totalTrainingCount = self.spamTrainingCount + self.hamTrainingCount
        
        for word in self.vocabList:
            self.wordSpamProbDict[word] = self.spamWordCount[word] / self.spamTrainingCount
            self.wordProbabilityDict[word] = (self.spamWordCount[word] + self.hamWordCount[word]) / self.totalTrainingCount
        
        # print self.spamWordCount
        # print self.hamWordCount
        # print self.wordSpamProbDict    
        return
    
if __name__ == "__main__":
    learn_obj = Learn()
    learn_obj.getData()
    learn_obj.find_token_probability()
    