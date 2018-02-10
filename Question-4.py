import glob, os
import re
import collections
import math
import random
from nltk.tokenize import sent_tokenize

#Taking input of all path
training_data_path= input("Enter Path of Training Data :")
test_data_path= input("Enter Path of Test Data :")
path= input("Enter Path where you want output files to be stored:")

def viterbi(line,states,trans,emission):
	#Splitting the given line into words
	words = line.split()

	#Find no of words
	length =len(words)

	#2d array to store the values
	V = [{}]
	POStags ={}

	#initializing for each state
	for state in states:

		#initializing the matrix
		V[0][state] = trans["start "+state]*emission[words[0]+"/"+state]
		POStags[state] = [state]

	#Calculating for each observed word
	for i in range(1,length):
		V.append({})
		newtags ={}

		#Calculating for each state
		for state in states:

			#taking  maximum over the extensions of all the paths that lead to the current state
			(prob, n_state) = max([(V[i-1][p_state] * trans[p_state+" "+state] * emission[words[i]+"/"+state], p_state) for p_state in states])
			V[i][state] = prob
			newtags[state] = POStags[n_state] + [state]
		POStags=newtags

	#taking  maximum over the extensions of all the paths that lead to the final state
	(prob, f_state) = max([(V[len(words) - 1][state], state) for state in states])


	return POStags[f_state]


#Changing directory to given path
os.chdir(training_data_path)
text=""
#getting all files
for file in glob.glob("*"):

	#opening files one by one
	with open(file,"r",encoding="ISO-8859-1") as f:

		#reading files one by one
		lines=f.readlines()
		for line in lines:

			#checking if there is no empty line
			if not len(line.strip()) == 0:

				#adding a start token and an end token to the beginning and the end of the sentence
				text= text+"/start "+line.strip().replace("\n","")+" /end\n "


#Splitting the text on basis of spaces to get word/tag counts
space_split_text = text.split()
word_tag_counter=collections.Counter()
word_tag_counter.update(space_split_text)

#Converting counter object to dictionary object
word_tag_dict  =dict(word_tag_counter)

#Printing data to a file
os.chdir(path)
with open(path+"/word_tag.txt","w+") as fu:
	fu.write(str(word_tag_dict))

#Splitting the text on basis of / to get tag unigram counts
tag_unigram_list =[]
tag_unigram_container=dict()
for words in space_split_text:

	#getting tags from each space split text
	tag = words.rsplit("/",1)[1]

	#appending tags to list
	tag_unigram_list.append(tag)

	#storing words associated to that tag
	if tag in tag_unigram_container.keys():
		tag_unigram_container[tag].append(words.rsplit("/",1)[0])
	else:
		tag_unigram_container[tag] = list()
		tag_unigram_container[tag].append(words.rsplit("/",1)[0])

#calculating tag unigram counts
tag_unigram_counter =collections.Counter()
tag_unigram_counter.update(tag_unigram_list)
tag_unigram_dict=dict(tag_unigram_counter)

#Printing data to a file
os.chdir(path)
with open(path+"/tag_unigram.txt","w+") as fu:
	fu.write(str(tag_unigram_dict))


tag_bigram_list=[]
tag_container=dict()

#Splitting tags in lines
line_text=text.split("\n")
for line in line_text:

	#Splitting lines to words
	words = line.split()

	#calculating tag bigram counts
	for i in range(len(words)-1):

		#adding tag bigram to list
		tag_bigram_list.append(words[i].rsplit("/",1)[1]+" "+words[i+1].rsplit("/",1)[1])

		tag=words[i].rsplit("/",1)[1]

		#Storing all next tags associated with this tag
		if tag in tag_container.keys():
			tag_container[tag].append(words[i+1].rsplit("/",1)[1])
		else:
			tag_container[tag] = list()
			tag_container[tag].append(words[i+1].rsplit("/",1)[1])

#calculating tag bigram counts
tag_bigram_counter=collections.Counter()
tag_bigram_counter.update(tag_bigram_list)
tag_bigram_dict=dict(tag_bigram_counter)

#Printing data to a file
os.chdir(path)
with open(path+"/tag_bigram.txt","w+") as fu:
	fu.write(str(tag_bigram_dict))

#Calculating tag Vocabulary for smoothing
tag_vocabulary= len(set(tag_unigram_list))

#Calculating Transition probability and doing smoothing
transition_probability_dict=collections.defaultdict(lambda: (1/tag_vocabulary))
for tag1 in set(tag_unigram_list):
	for tag2 in set(tag_unigram_list):
		tag_bigram=tag1+" "+tag2

		#Add one smoothing is done
		if tag_bigram in tag_bigram_dict.keys():
			transition_probability_dict[tag_bigram]= (tag_bigram_dict[tag_bigram]+1)/(tag_unigram_dict[tag_bigram.split()[0]]+tag_vocabulary)
		else:
			transition_probability_dict[tag_bigram] = (1/tag_vocabulary)

#Printing data to a file
os.chdir(path)
with open(path+"/transition_probability.txt","w+") as fu:
	fu.write(str(transition_probability_dict))

#Calculating emission probability and doing smoothing
emission_probability_dict=collections.defaultdict(lambda: (1/tag_vocabulary))
for word_tag in word_tag_dict.keys():
	emission_probability_dict[word_tag]=(word_tag_dict[word_tag]+1)/(tag_unigram_dict[word_tag.rsplit("/",1)[1]]+tag_vocabulary)

#Printing data to a file
os.chdir(path)
with open(path+"/emission_probability.txt","w+") as fu:
	fu.write(str(emission_probability_dict))

#Printing data to a file
os.chdir(path)
with open(path+"/random_sentence.txt","w+") as fu:
	i=0
	while(i<5):
		#initializing the values
		sentence=""
		probability=1
		nexttag="start"

		#Continue generating sentence till we get a end tag
		while(nexttag!="end"):

			#Randomly generate the word accounting emission probability
			nextword=""+random.choice(tag_unigram_container[nexttag])

			#Appending the word and tag to sentence
			sentence=sentence+" "+nextword+"/"+nexttag

			#Calculating the probability
			probability=probability*(emission_probability_dict[nextword+"/"+nexttag])
			previoustag=nexttag

			#Randomly generate the next tag accounting transition probability
			nexttag=""+random.choice(tag_container[nexttag])

			#Calculating the probability
			probability=probability*transition_probability_dict[previoustag+" "+nexttag]

		sentence =sentence+"/"+nexttag

		#Writing data to file
		fu.write(sentence +"\n Probability of generating this sentence is " +str(probability)+"\n")

		#Increasing the counter
		i=i+1



#Changing directory to given path
os.chdir(test_data_path)
testdata=""
#getting all .txt files
for file in glob.glob("*"):

	#opening .txt files one by one
	with open(file,"r",encoding="ISO-8859-1") as f:

		#reading files one by one
		lines=f.readlines()
		for line in lines:
			#checking if there is no empty line
			if not len(line.strip()) == 0:
				testdata= testdata+line

#tokenizing the data into sentences
testdata_lines=sent_tokenize(testdata)
testdata_foramt=list()

#combining two sentences if a sentence have less than 5 characters
for i in range(len(testdata_lines)):
	if(len(testdata_lines[i])<5):
		testdata_lines[i-1] = testdata_lines[i-1]+" "+testdata_lines[i]
		testdata_foramt.pop()
		testdata_foramt.append(testdata_lines[i-1])
	else:
		testdata_foramt.append(testdata_lines[i])

#Printing data to a file
os.chdir(path)
with open(path+"/POS_tagged_test_data.txt","w+") as fu:
	for j in range(len(testdata_foramt)):
		#Priniting sentence ID
		fu.write("<sentence ID=" + str(j+1) +">\n")

		#Calculating POS tags using viterbi algorithm
		POS=viterbi(testdata_foramt[j],set(tag_unigram_list),transition_probability_dict,emission_probability_dict)
		words =testdata_foramt[j].split()
		for i in range(len(words)):
			fu.write(words[i]+","+POS[i]+"\n")
		#Priniting EOS tag
		fu.write("<EOS>\n")
