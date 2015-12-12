# -*- coding: utf-8 -*-

import re
import string
from collections import OrderedDict, Counter, defaultdict

import operator

from NltkHelper import NltkHelper

title = "Reports Claim Satoshi Nakamoto Might Be 44-Year Old Australian"

content  = "New reports by Wired and Gizmodo may have identified the pseudonymous creator of bitcoin, Satoshi Nakamoto, as Australian entrepreneur Craig S Wright. "
content += "WIRED cites 'an anonymous source close to Wright' who provided a cache of emails, transcripts and other documents that point to Wright's role in the creation of bitcoin. Gizmodo cited a cache of documents sourced from someone claiming to have hacked Wright’s business email account, as well as efforts to interview individuals close to him."
content += "The news outlets further claimed that Dave Kleiman, a computer forensics expert who died in April 2013, played a significant role in the creation of bitcoin. According to Gizmodo, Kleiman 'seemed to be deeply involved with the currency and Wright’s plans' and may have a significant supply of bitcoins given his early role."
content += "It should be noted that, in WIRED’s case, the evidence was presented with caution that the information might be made up – perhaps even by Wright himself."
content += "Greenberg and Branwen write:"
content += "And despite a massive trove of evidence, we still can’t say with absolute certainty that the mystery is solved. But two possibilities outweigh all others: Either Wright invented bitcoin, or he’s a brilliant hoaxer who very badly wants us to believe he did."
content += "The idea that the Wright-Satoshi connection is nothing but a hoax has been floated by other observers, though the compelling nature of the evidence published by both Gizmodo and WIRED will no doubt fuel speculation for some time to come."
content += "But who is Wright exactly? A LinkedIn account attributed to Wright remains active at the time of writing, detailing work with a series of companies including Hotwire Pre-Emptive Intelligence Group – the firm behind an effort to create a bitcoin-based bank called Denariuz. That effort later ran into problems with the Australian Tax Office (ATO)."
content += "According to a presentation for the company published in June 2014, Denariuz aimed to become 'among the second tier banks in Australia within 5-6 years'."
content += "Gizmodo traced the connection between Wright and the ATO further, suggesting that Wright invoked his involvement in bitcoin's development during a meeting with agency officials."
content += "Further, the LinkedIn post suggests that Wright had a working relationship with representatives from various agencies within the US government."
content += "As part of work with a firm called the Global Institute for Cyber Security + Research, in a capacity as vice president and director for Asia-Pacific, Wright was responsible for fostering 'executive level relationships with the National Security Agency (NSA), Department of Homeland Security (DHS), North American Space Administration and DSD and regional government bodies'."
content += "Whether he is Satoshi or not, Wright appears to have taken efforts to reduce his online visibility by deleting his Twitter account, a move that came after the account was set to private. Gizmodo reported that the tweets were set private during its investigation."
content += "Wright did not immediately respond to a request for comment. A US phone number attributed to Wright in an email sent by him to CoinDesk in May did not connect when reached."



class TextAnalyzer:

    def __init__(self, title, content):
        self.title   = title
        self.content = content


    """
    Returns list of keywords
    Keyword: bigram found in both title and content that follows pattern (JJ, NN or FW) or (NN or FW, NN or FW) 
    """
    def getKeywords(self):
        #titles are in many cases all uppercase for first letter
        n1 = NltkHelper( self.title.lower() )
        formattedTitle = n1.preprocessTitle()

        n1 = NltkHelper( formattedTitle )
        n2 = NltkHelper( self.content )

        matches = list( set(n1.findTags()) & set(n2.findTags()) )
        return matches



    def cleanInput(self, input):
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

    def getWordsFrequency(self, input):
        input = self.cleanInput(input)
        map = Counter(input).most_common()
        return map
    

    def getExcerpt(self):
        words = self.content.split(" ")[:50]
        excerpt = " ".join(words)
        return excerpt


    def getNgramsFrequency(self, ngrams):
        map = defaultdict(int)

        for item in ngrams:
            map[ tuple(item) ] += 1

        #map = OrderedDict(map.items(), key=lambda t: t[1], reverse=True)
        #dict = Counter( map ).most_common()
        map = sorted(map.items(), key=lambda x:x[1], reverse=True)
        #map = OrderedDict(map.items(), key=lambda t: t[1], reverse=True)        

        return map

    

    def sortedNgrams( self, input, n):
        return self.sortFrequencies( self.ngrams(input, n) )
    
    """
    returns ngrams as dict key:lists, value: occurences
    """
    def ngrams(self, input, n):
        input = self.cleanInput(input)
        output = defaultdict(int)

        for i in range(len(input)-n+1):            
            key = " ".join( input[i:i+n] )
            output[ key ] += 1

        return output

    def sortFrequencies( self, ngrams):
        return sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True)


    def filterCommon(self, ngrams):
        output = []
        for item in ngrams:
            words = item[0].split(" ")
            for word in words:
                if not self.isCommon( word ):
                    output.append( item )
        return output

    def analyzeSentence(self, sentence):
        print sentence


    def isCommon(self, word):

        """
        The 100 most common words in English are:
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you",
        "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an" "will", "my", "one", 
        "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when",
        "make", "can", "like", "time", "no", "just", "him", "know", "take", "person", "into", "year", "your", "good", "some",
        "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back",
        "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", 
        "give", "day", "most", "us"
        """
        isCommon = [ "the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you",
                     "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an" "will", "my", "one", 
                     "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when",
                     "make", "can", "like", "time", "no", "just", "him", "know", "take", "person", "into", "year", "your", "good", "some",
                     "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back",
                     "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", 
                     "give", "day", "most", "us"]

        if word in isCommon:
            return True
        return False



    def ngramsAsTuples(self, input, n):
        input = self.cleanInput(input)

        output = []
        for i in range(len(input)-n+1):            
            output.append( input[i:i+n] )

        return output



#ta = TextAnalyzer( title, content)