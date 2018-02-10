This is readme file for question 4

How to run:
1. Install Pythonv3.6.4
2. Run the implementation by entering command on your command line python by command -
   python filename
3.The program asks
a)Enter Path of Training Data :
b)Enter Path of Test Data :
c)Enter Path where you want output files to be stored:

4. The count of tag unigram is stored in tag_unigram.txt
5. The count of word/tag is stored in word_tag.txt
6. The count of tag bigram is stored in tag_bigram.txt
7. Transition Probabilty are stored in transition_probability.txt
8. Emission Probabilty are stored in emission_probability.txt
9. Random Sentences generated using HMM is stored in random_sentence.txt
10.The output of viterbi algorithm is stored in POS_tagged_test_data

Implementation:
Programs takes input all training data and add starting and ending tag to sentences.
Word tag count is calculated by splitting data using spaces.
This word tag pairs are then seperated to calculate tag unigram count.
Every sentence is broken in words and transitions of tags in sentences are counted and stored in tag bigram
The above data is used to calculate transition and emission probability by using given formula and using add one smoothing.
  
Random Sentence Generator-
All words that are associated with a given tag are stored in a list repetation allowed
All tags that follow given tag are stored in a list repetation allowed.
Now we randomly choose next state/tag and then we randomly choose random word associated with that tag. 
As repetation is allowed the tags which have higher transition probability become more probable and words which have higher emission probability become higher probable.
Thus accounting transition and emission probability thus using hmm model and random techniques sentence is generated and its generation probability is calculated.

Viterbi algorithm 
The pseudo code given in book is reffered to implement the algorithm
The data is tokenized into sentences using NLTK sentence tokenizer
The sentence which were having length less tahn 5 character were appended back to pevious sentence to improve the efficiency.
To all the sentence the viterbi algorithm is applied.

Note:
All of these libraries are imported in program
import glob, os  - used to change directory
import re - used for regex
import collections - used for counting the data
import math - used for mathematical functions
from nltk.tokenize import sent_tokenize  - used for sentence tokenizing