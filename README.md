# Keyword-Extractor
Python text keyword finder based just on NLTK and Standford POSTagger. No training needed.
Given an article in English formed by title and content extract its keywords.

The algorithm used is as follows:
 1. Search bigrams in title formed by (ADJ-NN/FW) or (NN/FW-NN/FW)
 2. Search bigrams in content formed by (ADJ-NN/FW) or (NN/FW-NN/FW)
 3. Return the intersection of both sets

The Standord POStagger was used instead of the built-in NLTK tagger to make the syntactical analysis as it offered more accuracy on NN and FW detection than the NLTK-tagger.

## Next improvements
While this algorithm might miss some bygram keywords in the content, the result is preety good. For more results the next step would using IBM Watson web service.
