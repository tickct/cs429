#Python 2.7.3
import re
import os
import collections
import time

class index:
	def __init__(self,path):
               self.path=path
               self.fileDic=self.getFiles();
               self.lookupIndex={}
	def buildIndex(self):
                for id,inputFile in self.fileDic.iteritems():
                        file = open(self.path+"/"+inputFile,"r")
                        text=file.read()
                        cleanText=self.sanitizeAndTokenizeString(text)
                        fileIndex=self.getFileIndex(cleanText)
                        for word,locations in fileIndex.iteritems():
                                #since we are creating a dic per file first we dont need
                                #to worry about duplicate id's
                                if word in self.lookupIndex:
                                        self.lookupIndex[word].append((id,locations))
                                else:
                                        self.lookupIndex[word]=[(id,locations)]
        def getFileIndex(self,cleanText):
                locationInFile=1
                oneFileIndex={}
                for word in cleanText:
                        if word in oneFileIndex:
                                oneFileIndex[word].append(locationInFile)
                        else:
                                oneFileIndex[word]=[locationInFile]
                        locationInFile +=1
                return oneFileIndex
        def sanitizeAndTokenizeString(self,text):
                textSplit=text.split()
                textSplitClean=[]
                for token in textSplit:
                        cleanToken = re.sub('[^A-Za-z]+','',token).lower()
                        textSplitClean.append(cleanToken)
                return textSplitClean
        #Reads in all files in and map them to a dictionary since they dont get read in order
        #this dosn't really matter as long as we can rebind the ids to the correct file
        def getFiles(self):
                count=1
                files={}
                for itemName in os.listdir(self.path):
                     files[count]=itemName
                     count +=1
                return files
        def fPrint(self):
                for x in self.lookupIndex.items():
                        print x

	#def and_query(self, query_terms):
	#function for identifying relevant docs using the index

	#def print_dict(self):
        #function to print the terms and posting list in the index

	#def print_doc_list(self):
	# function to print the documents and their document id
collection = index("collection")
collection.buildIndex()
collection.fPrint()
