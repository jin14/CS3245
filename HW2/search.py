    import getopt
import sys
from Cacher import Cacher
import json
from nltk.stem.porter import PorterStemmer
import nltk
import math
import time

Operators = ['NOT', 'AND', 'OR']
precedence = {'(':4, ')':4, 'NOT':3, 'AND':2, 'OR':1}

stemmer = PorterStemmer()

def search(dictionary,postings,queries,output):


#   This is the main function that returns the query results and write it to the output file. 
#   It also has cachers instantiated to cache both the query results and intermediate query results.

    d = json.load(open(dictionary,'r'))
    p = open(postings)
    with open(queries) as q:
        with open(output,'w') as o:
            print("Querying ... ")
            querycacher = Cacher(20) # cacher for the queries
            mergingcacher = Cacher(50) # cacher for the intermediate merging of posting lists results 
            postingcacher = Cacher(100) # cacher for the postings lists results
            postingcacherNOT = Cacher(50) # cacher for the NOT x postings list results
            for query in q.read().splitlines():
                query = querytokenizer(query)
                query = shuntingyard(query)
                if querycacher.contains(' '.join(query)):
                    result = querycacher.get(' '.join(query))
                else:
                    result = process_query(query,d,p,postingcacher,postingcacherNOT,mergingcacher)
                    querycacher.update(' '.join(query),result)
                    
                #o.write(str(len(result)) + '\n')
                if len(result)>=1:
                    o.write(' '.join(map(str,result)) + '\n')

                else:
                    o.write('\n')



def isoperator(x):
    return x in Operators

def isleftbrace(x):
    return x == '('

def isrightbrace(x):
    return x == ')'

def shuntingyard(query):

##    This is the shunting yard method used to process the boolean search queries. 
##    It produces a postfix notation string that will be used to process the query

    
    operator = [] #stack to store all the operators
    output = [] #queue to store all the operands
    tokens = [token for token in query.split(' ') if token]
    for token in tokens:
        if not(isoperator(token) or isleftbrace(token) or isrightbrace(token)): 
            output.append(token)
            
            
        elif isleftbrace(token):
            operator.append(token)
        
        elif isrightbrace(token):
            
            try:
                while not (isleftbrace(operator[-1])):
                    output.append(operator.pop())
            
                operator.pop()
            except:
                print("Braces do not match, please check query.")

        elif isoperator(token):
            
            if len(operator)!=0:
                while len(operator)!= 0 and precedence[operator[-1]] > precedence[token] and not isleftbrace(operator[-1]):
                    output.append(operator.pop())

                operator.append(token)
            else:
                operator.append(token)
        
    while len(operator)!=0:
        output.append(operator.pop())
        
    
    return output




def process_query(newquery,dictionary,postings,postingcacher,postingcacherNOT,mergingcacher):

# This is the main function used to process the output from the shunting yard function, i.e the postfix notation
# This function identifies the right functions to call based on the operands and operators

   
    result = []
    sequence = []
    
    
    if len(newquery)==1: # if there is only one operand
        
        token = newquery[0]
        if postingcacher.contains(token): # check to see if its in the postings list
            result.append(postingcacher.get(token))
        else:
            ids = findpostings(token,dictionary,postings)
            postingcacher.update(token,ids)
            result.append(ids)

    elif len(newquery)==2: # if there is only 2 (should be a "NOT x" query)
        
        for token in newquery:
            if isoperator(token):
                
                if token == 'NOT':
                    previous = result.pop()
                    if postingcacherNOT.contains(previous): # check if its in the not-postings-list cacher
                        notresult = postingcacherNOT.get(previous)
                        result.append(notresult)
                    else:
                        notresult = notoperator(previous,dictionary,postings) # apply the not operator method to find the postings list
                        postingcacherNOT.update(previous,notresult)
                        result.append(notresult)
            else:
                result.append(token)
                
    else:
        index = 0
        while index < len(newquery):
            token = newquery[index]
            
            if isoperator(token):
                
                if token == 'NOT':
                    
                    if (index+1<len(newquery) and newquery[index+1]=='AND'): #this logic here is used to check if it is an AND NOT expression
                        
                        term1 = result.pop()
                        term2 = result.pop()
                        new = sequence[-2:] + [token,"AND"]
                        sequence = sequence[:-2]
                        sequence.append(new)
                        k = flatten(sequence[-1]) # flatten the list of lists so get the flat list of the query, so that we can hash the string of the query
                        query = ' '.join(k)
                        if mergingcacher.contains(query): # check if the query is present in the mergingcacher
                            mergingresult = mergingcacher.get(query)
                            result.append(mergingresult)
                        else:
                            mergingresult = skipANDNOT(term1,term2,token,dictionary,postings) # apply a faster method for AND NOT expression
                            mergingcacher.update(query,mergingresult) # store this new query in the mergingcacher
                            result.append(mergingresult)
                        
                        index+=1
                    
                    else:

                        previous = result.pop()
                        new = [sequence[-1]] + [token]
                        sequence = sequence[:-1]
                        sequence.append(new)
                        query = ' '.join(flatten(sequence[-1]))
                        
                        if postingcacherNOT.contains(query): # check if it is in the postingcacherNOT
                            notresult = postingcacherNOT.get(query)
                            result.append(notresult)
                        
                        else:
                            notresult = notoperator(previous,dictionary,postings) # apply the not operator
                            postingcacherNOT.update(query,notresult)
                            result.append(notresult)
                    
                    
                else:
                    term1 = result.pop()
                    term2 = result.pop()
                    new = sequence[-2:] + [token]
                    sequence = sequence[:-2]
                    sequence.append(new)
                    k = flatten(sequence[-1])
                    query = ' '.join(k)
                    if mergingcacher.contains(query): # check if the query is present in the mergingcacher
                        mergingresult = mergingcacher.get(query)
                        result.append(mergingresult)
                    else:
                        mergingresult = merge(term1,term2,token,dictionary,postings) # apply the merging step for AND and OR expressions
                        mergingcacher.update(query,mergingresult)
                        result.append(mergingresult)
                        
                index+=1
                    
            else:
                result.append(token)
                sequence.append(token)
                
                index+=1
    
    if len(result)>=1:
        return result[0]
    else:
        return result


def skipANDNOT1(left,right,token,dictionary,postings):

# This is for the AND NOT expression.
# eg. X AND NOT Y. This method will remove the docids that are found in Y from X if they share the same docids.


    if type(left)!=list:
        left = findpostings(left,dictionary,postings)
    if type(right)!=list:
        right = findpostings(right,dictionary,postings).copy()
    
    result = []
    
    if len(left) == 0:
        result = right

    else:
        while len(left)!=0 and len(right)!=0:
            if left[0] == right[0]:
                left = left[1:]
                right = right[1:]

            elif left[0] < right[0]:
                result.append(right[0])
                left = left[1:]

            elif left[0] > right[0]:
                result.append(right[0])
                right = right[1:]

        if len(right)!=0:
            result.extend(right)

    return result


def merge(left,right,operator,dictionary,postings):

# This is the merging step. It checks if the length is less than 4. If it is less than 4 theres is no point using a skiplist merging, 
#  hence we will just do a linear merging by going through every entry in both list.

    bound = 4
    
    if type(left)!=list:
        left = findpostings(left,dictionary,postings)
    if type(right)!= list:
        right = findpostings(right,dictionary,postings)
    
    if operator == 'AND':

        if len(left)< bound and len(right)< bound:
            result = []
            while len(left)!=0 and len(right)!=0:
                
                if left[0] == right[0]:
                    result.append(left[0])
                    left = left[1:]
                    right = right[1:]
                
                elif left[0]>right[0]:
                    right = right[1:]
                    
                elif left[0]<right[0]:
                    left = left[1:]
                
        else:
            result = skipintersectionAND(left,right) # calls the AND merging method
            
            
    
    elif operator == 'OR':
        
        result = intersectionOR(left,right)# calls the OR merging method

            
    
    return result
                       
def skipintersectionAND(left,right):

# This method imitates the nature of a skiplist. The index will skip if it is a modulo of the (len(list))**0.5
# It is an intersection method. 

    result = []
    i = 0
    j = 0
    skipI = math.floor(math.sqrt(len(left)))
    skipJ = math.floor(math.sqrt(len(right)))
    
    while len(left)>i and len(right)>j:

        if left[i] == right[j]:
            result.append(left[i])
            i+=1
            j+=1
        elif left[i] < right[j]:
            if not bool(i%skipI) and i+skipI < len(left) and left[i+skipI] <= right[j]:
                while not bool(i%skipI) and i+skipI < len(left) and left[i+skipI] <= right[j]:
                    i+=skipI
            else:
                i+=1
        
        elif left[i] > right[j]:
            if not bool(j%skipJ) and j+skipJ < len(right) and left[i] >= right[j+skipJ]:
                while not bool(j%skipJ) and j+skipJ < len(right) and left[i] >= right[j+skipJ]:
                    j+=skipJ
            else:
                j+=1
        
    return result


def intersectionOR(left,right):

# It is an union method. It goes through both list linearly and compares the output.

    result = []
    
    if len(left) == 0:
        result = right
    elif len(right) == 0:
        result = left
    else:
        while len(left)!=0 and len(right)!=0:
            if left[0] == right[0]:
                result.append(left[0])
                left = left[1:]
                right = right[1:]

            elif left[0] < right[0]:
                result.append(left[0])
                left = left[1:]

            elif left[0] > right[0]:
                result.append(right[0])
                right = right[1:]
    
        if len(left)!=0:
            result.extend(left)

        if len(right)!=0:
            result.extend(right)
    return result
    
def notoperator(previous,dictionary,postings):

# NOT x method. This method returns the dictionary ids that are not found in x.

    if type(previous)!=list:
        previous = findpostings(previous,dictionary,postings)
    
    return [i for i in dictionary["ids"] if i not in previous]



def findpostings(term,dictionary,postings):

# this is the main method used to find the postings list. 
# It first finds the starting byte of the term from the dictionary and based on the length, it seeks the postings file for the docids.

    if term in dictionary:
        start = dictionary[term]['s']
        length = dictionary[term]['l']
        postings.seek(start)
        result = list(map(int,postings.read(length).split(',')))

    else:
        result = []
        
        
    return result
        
def querytokenizer(query):

# this is a tokenizer for the query to ensure that it goes through the same preprocessing step as the indexing phase 

    query = query.replace('(', ' ( ')
    query = query.replace(')', ' ) ')

    for token in [ i for i in query.split(' ') if i]:
        if token not in ["AND","OR","NOT","(",")"]:
            query = query.replace(token,tokenize(token)[0])
            
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

def flatten(lst):

# this is used to flatten the list

    return sum( ([x] if not isinstance(x, list) else flatten(x) for x in lst), [] )


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
