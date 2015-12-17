# Keyword-Extractor
Python text keyword extractor based just on NLTK Pos Tagger

## Given an article in English formed by title and content extract its keywords.
The algorithm used is as follows:
1) Search bigrams in title formed by (ADJ-NN/FW) or (NN/FW-NN/FW)
2) Search bigrams in content formed by (ADJ-NN/FW) or (NN/FW-NN/FW)
3) Return the intersection of both sets

##Standord POS tagger was used instead of the built-in NLTK tagger.
