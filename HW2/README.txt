This is the README file for A0139100X's submission
e0002985@u.nus.edu
== Python Version ==

I'm using Python Version 3.5.2 for this assignment.

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

Steps to build index.py:

To carry out the indexing phase, I used a dictionary with the terms as the keys and the postings list as the values.
The dictionary file is being written in a json format, with the consideration that I would be able to find the necessary information I need for a term in O(1) time. An entry in the dictionary file would resemble something like this:
{‘the’:{’s’:10, ‘l’:100 },…..}

The ’s’ is used to indicate the starting byte of the term in the postings file while the ‘l’ is used to indicate the size so that during the searching phase, the program will know when to stop seeking.

The postings file is a file of number with the numbers comma separated. The commas are used to distinguish 1,2,11,14,20 … This is because, without the commas, I faced the difficulty of identify 1123. Is it 11,23 or 1123 or 1,123? To tackle this problem, I decided to use commas to differentiate them, even though it might take extra space.


Steps to build the search.py(Search function):

The first step I took was to build a shunting yard function to process the nefarious boolean query expressions. This helped to ensure that the operators are being processed in the correct order.

Thereafter, I had to process the postfix notation outputted by the shunting yard algorithm.

“AND NOT”: for AND NOT queries, the function is slightly optimised as we only have to remove terms that are found in one list from another list

“AND/OR”: this operation was implemented with a skip list. AND is an intersection while OR is an union

“NOT”: this is used for NOT x queries

I also implemented a cacher class. This is used to cache the queries that the user make. This is to optimise the search function so that if a similar search query has been made before, it does not have to go through the tedious tasks of searching and merging the postings list again.

The dictionary file is being loaded in the json format for easy access.


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

index.py: This is the file with the code for the indexing phase.

search.py: This is the file to process the queries and return the output

ESSAY.txt: Answers to all the essay ins

Cacher.py: Cacher class for optimisation

README.txt: short write up of the entire assignment, which is this file.


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

How to implement shunting yard algorithm: https://en.wikipedia.org/wiki/Shunting-yard_algorithm, http://www.oxfordmathcenter.com/drupal7/node/628, https://brilliant.org/wiki/shunting-yard-algorithm/

How to use nltk tokeniser: http://www.nltk.org/book/ch03.html

Skip list implementation: Introduction to Information Retrieval - Stanford NLP Group chapter 2

How to flatten a list:
http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python




