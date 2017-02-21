#Python 3.0
import re
import os
import collections
import time
#import other modules as needed

class index:
        def __init__(self,path):
                self.path=path
                self.fileDic=self.getFiles();
                self.stopDic=self.getStop();
                #using defaultdict saves us build time
                self.lookupIndex=collections.defaultdict(list)
        def buildIndex(self):
                for id,inputFile in self.fileDic.items():
                        file = open(self.path+"/"+inputFile,"r")
                        text=file.read()
                        cleanText=self.sanitizeAndTokenizeString(text)
                        fileIndex=self.getFileIndex(cleanText)
                        for word,locations in fileIndex.items():
                                #since we are creating a dic per file first we dont need to worry about duplicate id's
                                self.lookupIndex[word].append((id,locations))
        #creates a dictionary of format {word:[loc]} for a given token list which comes from one file, since it is one file we can ignor the file id field until we merge with the lookupIndex
        def getFileIndex(self,cleanText):
                locationInFile=1
                oneFileIndex={}
                for word in cleanText:
                        if word not in self.stopDic:
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
        def getStop(self):
                file = open('stop-list.txt',"r")
                text=file.read()
                stopList=text.split()
                return stopList
        def and_query(self, query_terms):
                lookupHolder=[]
                for word in query_terms:
                        #doing this slows down the querry but speeds up any querry that has an illigal term
                        if(word in self.lookupIndex.keys()):
                                lookupHolder.append([ids[0] for ids in self.lookupIndex[word]])
                        else:
                                print (word, "not found in any files -no match possible")
                                return
                matchAll=reduce(self.indexMatch,lookupHolder)
                for x in matchAll:
                        print (self.fileDic[x])
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

	#def exact_query(self, query_terms, k):
	#function for exact top K retrieval (method 1)
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
	
	#def inexact_query_champion(self, query_terms, k):
	#function for exact top K retrieval using champion list (method 2)
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
	
	#def inexact_query_index_elimination(self, query_terms, k):
	#function for exact top K retrieval using index elimination (method 3)
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
	
	#def inexact_query_cluster_pruning(self, query_terms, k):
	#function for exact top K retrieval using cluster pruning (method 4)
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

        def print_dict(self):
                for x in self.lookupIndex.items():
                        print (x)
        #prints the document list and there id's

        def print_doc_list(self):
                for x in self.fileDic.items():
                        print (x)


collection=index("collection")
collection.buildIndex()
collection.print_dict()
