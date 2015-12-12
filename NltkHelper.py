# -*- coding: utf-8 -*-

from nltk import Text, word_tokenize, sent_tokenize, pos_tag, ngrams, FreqDist

from nltk.corpus import wordnet as wn
import os, sys
from os.path import expanduser

from nltk.tag.stanford import StanfordPOSTagger

from collections import  defaultdict

import operator
import re, string


class NltkHelper:

	def __init__(self, text):
		reload(sys)  
		sys.setdefaultencoding('utf8')

		self.text = text

		root = os.path.dirname(os.path.realpath(__file__))
		os.environ["STANFORD_PARSER"] = root+"/stanford-postagger/stanford-postagger.jar"
		os.environ["STANFORD_MODELS"] = root+"/stanford-postagger/models/"
		
		
		_path_to_model  = root + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
		_path_to_jar    = root + '/stanford-postagger/stanford-postagger.jar'
		self.stanford   = StanfordPOSTagger(_path_to_model, _path_to_jar)

		self.sentences  = sent_tokenize(text.encode("utf-8"))
		self.words      = word_tokenize(text.encode("utf-8"))
		

		self.tags = self.stringifyTuples(self.stanford.tag( word_tokenize(text.lower()) ))
		#cleanWords = self.cleanWords()
		#self.tags = self.stringifyTuples(self.stanford.tag( cleanWords ))
		#print self.cleanWords()
		
		self.taggedBigrams = self.ngramsAndTags(2) 

		#print self.words
		#print self.cleanWords()
		
		#print "Bigrams --> ", self.taggedBigrams
		#print "Tags --> ", self.findTags()
		
		#print (nouns)
	
	def personal_names(self):
		output = []

		#(('reports', 'NNS'), ('claim', 'VBP'))
		for gram in self.taggedBigrams:
			tag1  = gram[0][1]
			tag2  = gram[1][1]
			word1 = gram[0][0]
			word2 = gram[1][0]

			if self.isPersonalName( tag1 ) and self.isPersonalName( tag2 ):
				output.append( "{0} {1}".format(word1, word2) )
		return output

	def isPersonalName(self, tag):
		return tag == "NNP" or tag == "FW"

	
	def preprocessTitle(self):
		
		output = ''
		for taggedWord in self.tags:
			
			word = taggedWord[0]
			tag  = taggedWord[1]

			if self.isPersonalName(tag):
				output = "{0} {1}".format(output, word.title())
			else:
				output = "{0} {1}".format(output, word.lower())


		return output
	
	def ngramsAndTags(self, n):
		output = []
		for i in range(len(self.tags)-n+1):
			gram = (self.tags[i],)
			for j in range(i+1, i+n):
				gram += ( self.tags[j], )
	    		output.append( gram )

		return output
	


	def sortFrequencies( self, ngram ):
		return sorted(ngram.items(), key = operator.itemgetter(1), reverse=True)		    
    

	
	def findTags(self):
		#pattern = [("AJ", NOUN/S/FWS), (FW, FW), NOUN, NOUN]
		output = []

		#(('reports', 'NNS'), ('claim', 'VBP'))
		for gram in self.taggedBigrams:
			tag1  = gram[0][1]
			tag2  = gram[1][1]
			word1 = gram[0][0]
			word2 = gram[1][0]

			if self.isAdj( tag1 ) and self.isNounOrForeignWord( tag2 ) or self.isNounOrForeignWord( tag1 ) and self.isNounOrForeignWord( tag2 ):
				output.append( "{0} {1}".format(word1, word2) )
		return output


	def isAdj(self, tag):
		return tag=='JJ'

	def isNounOrForeignWord(self, tag):
		nouns = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']
		return tag in nouns

	"""
	def bigramsList(self):		
		pass
	"""
	def stringifyList(self, list):
		output = []
		for tag in list:
			output.append( str(tag.encode('utf-8')) )
		
		return output

	def stringifyTuples(self, tuples):
		output = []
		for tag in tuples:
			output.append( (str(tag[0].encode('utf-8')), str(tag[1].encode('utf-8'))) )
		
		return output


	"""
	returns list of tuples of tagged words in text
	"""
	def analyze(self):
		output = []
		for sentence in self.sentences:
			taggedWords = self.stanford.tag( word_tokenize( sentence.lower() ) )
			output.append(taggedWords)

		return self.stringifyTuples(taggedWords)

	"""
	returns list of nouns and foreign words
	"""
	def filterNounsInText(self):
		output = set()
		nouns = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']

		for sentence in self.sentences:
			taggedWords = self.stanford.tag( word_tokenize(sentence.lower() ) )
			for item in taggedWords:
				if item[1] in nouns:
					output.add( item[0] )
		
		return self.stringifyList( list(output) )

	



	def cleanWords(self):
		input = ''
		for item in self.words:
			input = "{0} {1}".format(input, item)

		input = re.sub('\n+', " ", input)
		input = re.sub('\[[0-9]*\]', "", input)
		input = re.sub(' +', " ", input)
		input = bytes(input)
		input.decode('ascii', 'ignore')

		input = input.split(" ")
		cleanInput = []

		for item in input:
			item = item.strip( string.punctuation )

			if len(item)>1 or (item.lower()=='a' or item.lower()=='i'):
			    cleanInput.append( item )

		return cleanInput



	def bigramNouns(self, text):
		nouns = self.filterNouns(text)		
		
		

	def isTagNounOrForeignWord(self, word):
		output = False
		nouns = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']
		taggedWords = self.stanford.tag( word.lower()  )
		for item in taggedWords:
			if item[1] in nouns:
				output = True
				break
		return output

	@staticmethod
	def filterNouns(self, input):
		output = set()
		nouns = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']
		sentences = sent_tokenize(input)
		for sentence in sentences:
			taggedWords = self.stanford.tag( word_tokenize(sentence.lower() ) )
			for item in taggedWords:
				if item[1] in nouns:
					output.add( item[0] )
		nList = list(output)
		return self.stringifyTuples(nList)

	@staticmethod
	def define( self, word ):	

		definitions = []	
		try:
			synsets = wn.synsets(word)
			for synset in synsets:
				definitions.append (synset.definition())
		except ValueError:
			print "Cannot define '{0}'".format(word)

		return definitions

	def sentenceExamples( self, noun):
		output = []
		try:
			synsets = wn.synsets(noun)
			for synset in synsets:
				examples = synset.examples()
				for example in examples:
					output.append( example )
		except ValueError, AttributeError:
			print "Cannot find any example for '{0}'".format(noun)

		return output


	def filterPersonalNouns(self, input):
		output = set()
		pNouns = ['NNP', 'NNPS', 'FW']

		sentences = sent_tokenize(input)
		for sentence in sentences:
			taggedWords = self.stanford.tag( word_tokenize( sentence.lower() ) )
			for item in taggedWords:
				if item[1] in nouns:
					output.add( item[0] )

		return list(output)


title = "Reports Claim Satoshi Nakamoto Might Be 44-Year Old Australian"

content  = "New reports by Wired and Gizmodo may have identified the pseudonymous creator of bitcoin, Satoshi Nakamoto, as Australian entrepreneur Craig S Wright. "
content += "WIRED cites 'an anonymous source close to Wright' who provided a cache of emails, transcripts and other documents that point to Wright's role in the creation of bitcoin. Gizmodo cited a cache of documents sourced from someone claiming to have hacked Wright’s business email account, as well as efforts to interview individuals close to him. "
content += "The news outlets further claimed that Dave Kleiman, a computer forensics expert who died in April 2013, played a significant role in the creation of bitcoin. According to Gizmodo, Kleiman 'seemed to be deeply involved with the currency and Wright’s plans' and may have a significant supply of bitcoins given his early role. "
content += "It should be noted that, in WIRED’s case, the evidence was presented with caution that the information might be made up – perhaps even by Wright himself. "
content += "Greenberg and Branwen write: "
content += "And despite a massive trove of evidence, we still can’t say with absolute certainty that the mystery is solved. But two possibilities outweigh all others: Either Wright invented bitcoin, or he’s a brilliant hoaxer who very badly wants us to believe he did. "
content += "The idea that the Wright-Satoshi connection is nothing but a hoax has been floated by other observers, though the compelling nature of the evidence published by both Gizmodo and WIRED will no doubt fuel speculation for some time to come. "
content += "But who is Wright exactly? A LinkedIn account attributed to Wright remains active at the time of writing, detailing work with a series of companies including Hotwire Pre-Emptive Intelligence Group – the firm behind an effort to create a bitcoin-based bank called Denariuz. That effort later ran into problems with the Australian Tax Office (ATO). "
content += "According to a presentation for the company published in June 2014, Denariuz aimed to become 'among the second tier banks in Australia within 5-6 years'. "
content += "Gizmodo traced the connection between Wright and the ATO further, suggesting that Wright invoked his involvement in bitcoin's development during a meeting with agency officials. "
content += "Further, the LinkedIn post suggests that Wright had a working relationship with representatives from various agencies within the US government. "
content += "As part of work with a firm called the Global Institute for Cyber Security + Research, in a capacity as vice president and director for Asia-Pacific, Wright was responsible for fostering 'executive level relationships with the National Security Agency (NSA), Department of Homeland Security (DHS), North American Space Administration and DSD and regional government bodies'. "
content += "Whether he is Satoshi or not, Wright appears to have taken efforts to reduce his online visibility by deleting his Twitter account, a move that came after the account was set to private. Gizmodo reported that the tweets were set private during its investigation. "
content += "Wright did not immediately respond to a request for comment. A US phone number attributed to Wright in an email sent by him to CoinDesk in May did not connect when reached."


"""
n1 = NltkHelper( title.lower() )

formattedTitle = n1.preprocessTitle()
print "Title ", formattedTitle
n1 = NltkHelper( formattedTitle )

print '\n----\n'

n2 = NltkHelper( content )


print "Matches: ",list( set(n1.findTags()) & set(n2.findTags()) )

print n2.personal_names()
"""