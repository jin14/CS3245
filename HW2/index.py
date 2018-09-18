from nltk.stem.porter import PorterStemmer
import os
import string
import nltk
import getopt
import sys
import re
import json
from collections import OrderedDict

stemmer = PorterStemmer()

def make_dictionary(directory,dictionary_file, postings_file):

##    This function creates a dictionary with the terms as the key and the postings lists as the value. 
##   The keys are written to a dictonary file while the values are written to a postings file.

    filepaths = os.listdir(directory) # get the directories
    results = {}
    ids = []
    for filepath in sorted(filepaths,key=int): ## testing , rmb to remove when submitting 
        ids.append(int(filepath))
        with open(directory+filepath,'r') as file:
            for line in file:
                sent = [nltk.word_tokenize(tokens) for tokens in nltk.sent_tokenize(line)] # tokenisation
                for tokens in sent:
                    for token in tokens:
                        token = stemmer.stem(token.lower()) # stemming and lowercase

                        # if bool(re.search(r'\d', token)): # normalisation of numbers for essay qn
                        #     token = 'num'

                        if token not in results:
                            results[token] = {'postings':{filepath:1}}

                        elif filepath not in results[token]['postings']:
                            results[token]['postings'][filepath] = 1

                        else:
                            results[token]['postings'][filepath]+=1



    dictionary = open(dictionary_file, 'w')
    postings = open(postings_file,'w')
    new = {}
    new["ids"] = ids
    print("Creating dictionary and postings list file....")
    for token,docids in results.items():
        start = postings.tell() # get the starting byte of the postings file
        posting = ','.join(map(str,docids))
        postings.write(posting)
        new[token]={"s":start,"l": len(posting)} # store the starting byte and the length of the file
    
    json.dump(new,dictionary)
    print("Size of dictionary: " + str(len(results.keys())) + " words")
    dictionary.close()
    postings.close()


def usage():
    print ("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

directory_of_documents = dictionary_file = postings_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except (getopt.GetoptError, err):
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        directory_of_documents = a
    elif o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"
if directory_of_documents == None or dictionary_file == None or postings_file == None:
    usage()
    sys.exit(2)


make_dictionary(directory_of_documents, dictionary_file, postings_file)
