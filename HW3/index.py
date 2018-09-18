from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords as sw
import os
import string
import nltk
from collections import OrderedDict
import json
import math
from util import tf,L2norm
import sys
import getopt
import time

stemmer = PorterStemmer()

def make_dictionary(directory,dictionary_file,postings_file):
    filepaths = os.listdir(directory) # get all the directories
    results = {}
    ids = []
    for filepath in sorted(filepaths,key=int):
        ids.append(int(filepath))
        with open(directory+filepath,'r') as file:
            for line in file:
                sent = [nltk.word_tokenize(tokens) for tokens in nltk.sent_tokenize(line)] #sent tokenisation and word tokenisation
                for tokens in sent:
                    for token in tokens:
                        token = stemmer.stem(token.lower())
                        if token not in results:
                            results[token]= {'postings':{filepath:1}} # add in the docid and the natural term frequency
                        
                        elif filepath not in results[token]['postings']:
                            results[token]['postings'][filepath] = 1
                        
                        else:
                            results[token]['postings'][filepath] +=1
                        
            length = [] # store all the log frequency of the terms in a document
            for token in results: 
                if filepath in results[token]['postings']:
                    tfreq = tf(results[token]['postings'][filepath])  # convert all the natural term frequency to logarithmic term frequency
                    results[token]['postings'][filepath] = tfreq
                    length.append(tfreq)
            
            for token in results: # convert all the log term frequency into normalised term frequency, lnc
                if filepath in results[token]['postings']:
                    results[token]['postings'][filepath] = results[token]['postings'][filepath]/L2norm(length)
            
            
            
            
    #get all the idfs for all the terms which will be used in calculating the tfidf value of the query terms            
    for token in results:
        results[token]['idf'] = math.log10(len(filepaths)/len(results[token]['postings']))
        
    
    dictionary = open(dictionary_file,'w')
    postings = open(postings_file,'w')
    new = {}
    for term,info in results.items():
        start = postings.tell()
        line = ''
        for docid,termf in info['postings'].items():
            line+=docid + ',' + str(termf) +' '
        postings.write(line)
        new[term]={'s':start,'l':len(line),'i':info['idf']}
    
    json.dump(new,dictionary)
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


start = time.time()
print("Creating index...")
make_dictionary(directory_of_documents, dictionary_file, postings_file)
end = time.time()
print("Time taken to index: " + str(end-start))
