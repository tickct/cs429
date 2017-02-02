#Python 2.7.3
import re
import os
import collections
import time
import timeit

class index:
	def __init__(self,path):
               self.path=path
               self.fileDic=self.getFiles();
               #using defaultdict saves us .05 sec build time
               self.lookupIndex=collections.defaultdict(list)
               
        #opens all files in the fileDic one at a time sanitizes them, creates a single doc index then merges it with the lookupIndex       
	def buildIndex(self):
                for id,inputFile in self.fileDic.iteritems():
                        file = open(self.path+"/"+inputFile,"r")
                        text=file.read()
                        cleanText=self.sanitizeAndTokenizeString(text)
                        fileIndex=self.getFileIndex(cleanText)
                        for word,locations in fileIndex.iteritems():
                                #since we are creating a dic per file first we dont need to worry about duplicate id's
                                self.lookupIndex[word].append((id,locations))
        #creates a dictionary of format {word:[loc]} for a given token list which comes from one file, since it is one file we can ignor the file id field until we merge with the lookupIndex
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
        #splits string into tokens, uses regular expressions to then clean it into only alpha strings and return as a list of them in lower case
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
        #takes in a list of terms, fetches doc lists for each term then applies folds them with index match
        #since A&B&C == (A&B)&C if we find the matches for 2 items we can then match the result with the next item
	def and_query(self, query_terms):
                lookupHolder=[]
                for word in query_terms:
                        #doing this slows down the querry by ~.003 seconds but speeds up any querry that has an illigal term
                        if(word in self.lookupIndex.keys()):
                                lookupHolder.append([ids[0] for ids in self.lookupIndex[word]])
                        else:
                                print word, "not found in any files -no match possible"
                                return
                matchAll=reduce(self.indexMatch,lookupHolder)
                for x in matchAll:
                        print self.fileDic[x]
                        
        #matches 2 arrays common files by comparing and incramenting whichever vaule is lower so it only traverses once        
        def indexMatch(self,array1,array2):
                pointers=[0,0]
                matches=[]
                while(pointers[0]<len(array1) and pointers[1]<len(array2)):
                #match add to matches and increasse both pointers
                        
                       
                        if(array1[pointers[0]]==array2[pointers[1]]):
                               matches.append(array1[pointers[0]])
                               pointers[0]+=1
                               pointers[1]+=1
                #array1 number is greater increase array 2 pointer
                        elif(array1[pointers[0]]>array2[pointers[1]]):
                               pointers[1]+=1
                        else:
                               pointers[0]+=1
                return matches
        #function to print the terms and posting list in the index
        def print_dict(self):
        
                for x in self.lookupIndex.items():
                        print x
        #prints the document list and there id's
	def print_doc_list(self):
	        for x in self.fileDic.items():
                        print x
                        
buildStartTime=time.clock()
collection = index("collection")
collection.buildIndex()
buildEndTime=time.clock()-buildStartTime
print "collection built in :",buildEndTime
query=raw_input("enter search terms or -1 to quit:")
while(query != "-1"):       
        queryStartTime=time.clock()
        collection.and_query(query.split())
        queryEndTime=time.clock()-queryStartTime
        print "querry retrived in :",queryEndTime
        query=raw_input("enter search terms or -1 to quit:")
