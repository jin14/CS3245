This is the README file for A0139100X's submission
e0002985@u.nus.edu
== Python Version ==

I'm using Python Version 3.5.2 for this assignment.

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

I worked with the code from my assignment 2 and tried to make as little changes as possible.

Steps to build index.py:

Constructing the dictionary:
The dictionary file is stored in the json format for easy access during the searching phase. The structure of the dictionary file looks like this:
“Term”:{“l”: length_of_entry_in_postings_file, “i”:the_idf_of_the_term, “s”: starting_byte _in_the_postingsfile}, …
The idf of each term is calculated during the indexing phase using math.log10(total_number_of_docs/number_of_docs_containing_term)
The starting byte and length is stored for easy access during the searching phase so that seek could be used.

Constructing the postings file:
The structure of the postings file differ slightly from assignment 2. In this assignment, the postings file is modified to stored the docid for each term as well as its normalised logarithmic term frequency. The structure looks something like this
Docid1,normalised_tf_value1 Docid2,normalised_tf_value2 Docid3,normalised_tf_value3
They are comma separated and docid,normalisedtf pair is separated by a space for easy differentiation. This contributes to the large size of the file.


Steps to build the search.py(Search function):

The search.py file is slightly different from assignment 2. In this assignment, for each query, the tfidf values are calculated. For each term in the query we then proceed to find the dcoument that contains them and calculate the score based on the lnc.ltc scheme. There is an inherent implementation of an OR query since it is a free text query where as long as the document contains at least one word in the query, it will be factored into the pool of documents to be ranked and retrieved.


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

index.py: This is the file with the code for the indexing phase.

search.py: This is the file to process the queries and return the output

ESSAY.txt: Answers to all the essay qns

Cacher.py: Cacher class for optimisation

README.txt: short write up of the entire assignment, which is this file.

util.py: contains all the mathematical functions needed to calculate the lnc.ltc values

dictionary.txt: the dictionary file created during the indexing phase

postings.txt: the postings file created during the indexing phase

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0139100X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

Information retrieval book Chapter 6 for reference on answering essay questions as well as the lnc.ltc scheme

How to use a heap in python: https://docs.python.org/2/library/heapq.html

Log function in python: https://docs.python.org/2/library/math.html

Understanding how Euclidean distance normalisation does not factor in length of document:
https://www.cs.cornell.edu/courses/cs6740/2010sp/guides/lec03.pdf

Talked to Lim Jie, Peng Cheng about implementation of L2norm

