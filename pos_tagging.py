# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis

# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

#import pandas as pd
#x = pd.read_csv('sentences.txt', index_col=0)
#print(x)
#   ____________________________________________________
#  |   springs|NNS on|IN the|DT eastern|NN edge|NN of   |
#  |___________________________________________________ |

def unchanging_plurals():
    unchanging_nouns = []
    NNlist = []
    NNSlist = []
    with open("sentences.txt", "r") as f:
        for line in f:
            for tupple in line.split():
                #print(tupple)
                (noun, type) = tupple.split("|")
                if(type == 'NN' and noun not in NNlist):
                    NNlist.append(noun)
                if(type == 'NNS' and noun not in NNSlist):
                    NNSlist.append(noun)
    for noun in NNSlist:
        if(noun in NNlist):
            unchanging_nouns.append(noun)
    return unchanging_nouns


#UnchangingPlurals = unchanging_plurals()
#print(UnchangingPlurals)
#unchanging_plurals()


def noun_stem (s):
    #extracts the stem from a plural noun, or returns empty string
    if s in UnchangingPlurals:
        return s
    elif (re.match("\w*(men)$", s)):
        return s[:-2] + "an"
    elif (re.match("\w*([^(ch)(sh)aeiou])s$", s)):
        infinitive = s[:-1]
    elif(re.match("\w*([aeiou])ys$", s)):
        return s[:-1]
    elif (re.match("\w*([^aeiou])ies$", s) and len(s) >=5):
        return s[:-3] + "y"
    elif (re.match("[^aeiou]ies$", s)):
        return s[:-1]
    elif (re.match("\w*([(ch)(sh)(zz)(ss)ox])es$", s)):
        return s[:-2]
    elif (re.match("\w*([^s][s])es$", s) or re.match("\w*([^z][z])es$", s)):
        return s[:-1]
    elif (re.match("has", s)):
        return "have"
    elif (re.match("\w*([^(ch)(sh)iosxz])es$", s)):
        return s[:-1]
    else:
        return ""



def tag_word (lx,wd):
    #returns a list of all possible tags for wd relative to lx"""
    lex = []
    
    for token in lx.getAll("P"):
        if wd == token:
            lex.append("P")
    for token in lx.getAll("A"):
        if wd == token:
            lex.append("A")
    for token in lx.getAll("N"):
        if noun_stem(wd) == token:
            lex.append("Np")
        if wd == token:
            lex.append("Ns")
    for token in lx.getAll("I"):
        if verb_stem(wd) == token:
            lex.append('Is')
        elif wd == token:
            lex.append("Ip")
    for token in lx.getAll("T"):
        if verb_stem(wd) == token:
            lex.append("Ts")
        elif wd == token:
            lex.append("Tp")

    for (token, type) in function_words_tags:
        if (wd == token):
            lex.append(type)
    return lex



def tag_words (lx, wds):
    #returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
