import heapq
from collections import Counter
from nltk.stem.porter import PorterStemmer
import os
import nltk
import json
import math
from util import tf,L2norm
import sys
import getopt
import time
from Cacher import Cacher


stemmer = PorterStemmer()

def search(dictionary,postings,queries,output):


#   This is the main function that returns the query results and write it to the output file. 
#   It also has cachers instantiated to cache both the query results.

    d = json.load(open(dictionary,'r'))
    p = open(postings)
    queryCacher = Cacher(100) # used to cache the queries
    with open(queries) as q:
        with open(output,'w') as o:
            print("Querying ... ")
            for query in q.read().splitlines():
                if queryCacher.contains(query): #check if it has been queryed for previously
                    result = queryCacher.get(query) 
                    o.write(result + '\n')
                else:
                    queryS = queryscore(query,d) # ltc scheme for query
                    result = {}
                    tfs = {}
                    for word in tokenize(query):
                        if word in d:
                            postingswithtf = getpostings(d,p,word) # find the postings for the term
                            for docid in postingswithtf:

                                if docid in result:
                                    result[docid] += float(postingswithtf[docid]) * queryS[word] # calculate the lnc.ltc scores
                                elif docid not in result:

                                    result[docid] = float(postingswithtf[docid]) * queryS[word]
                
                    heap = [(value, key) for key,value in result.items()]
                    # get the top 10 document id based on the lnc.ltc score
                    result = heapq.nlargest(10, heap)
                    result = [(key,value) for value, key in result]
                    result = ' '.join(map(str,[i[0] for i in result]))
                    queryCacher.update(query,result)
                    o.write(result + '\n')
    p.close()
                    

def queryscore(query,dic):
    query = Counter(tokenize(query))
    for word in query:
        #LTC
        if word in dic:
            query[word] = (tf(query[word])/L2norm(map(tf,query.values())))* dic[word]['i']
        else:
            query[word]=0
                
    
    return query

def stem_tokens(tokens, stemmer):

# this is the stemming method to stem a list of tokens

    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item.lower()))
    return stemmed


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    #lemmatizer = WordNetLemmatizer()
    #word = lemmatizer.lemmatize(tokens)
    return stems

def getpostings(dictionary,postings,term):
    #get the postings list and its normalised tf value of the term from the postings file
    start = dictionary[term]['s']
    length = dictionary[term]['l']
    postings.seek(start)
    results = postings.read(length-1)
    return dict(list(k.split(',')) for k in results.split(' '))                     


def usage():
    print ("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

dictionary_file = postings_file = file_of_queries = output_results = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except (getopt.GetoptError, err):
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        output_results = a
    else:
        assert False, "unhandled option"
if dictionary_file == None or postings_file == None or file_of_queries == None or output_results == None: 
    usage()
    sys.exit(2)

start = time.time()
search(dictionary_file,postings_file,file_of_queries,output_results)
end = time.time()
print("Time taken: " + str(end-start))

       