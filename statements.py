# File: semantics.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised October 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu with help from Kiniorski Filip


# PART A: Processing statements
from nltk.corpus import brown

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    #stores known word stems of various part-of-speech categories
    def __init__ (self):
        self.TokenList = []
    def add (self, stem, cat):
        self.TokenList.append((stem, cat))
    def getAll (self, cat):
        stems = []
        for pair in self.TokenList:
            if (pair[1] == cat):
                add(stems, pair[0])
        return stems

#lx = Lexicon()
#lx.add("John", "P")
#lx.add("Marry", "P")
#lx.add("like", "T")
#lx.add("like", "P")
#lx.getAll("P")

class FactBase:
    #stores unary and binary relational facts
    def __init__ (self):
        self.featuresList = []
    def addUnary (self, pred, e1):
        self.featuresList.append((pred, e1))
    def addBinary (self, pred, e1, e2):
        self.featuresList.append((pred, e1, e2))
    def queryUnary (self, pred, e1):
        return (pred, e1) in self.featuresList
    def queryBinary (self, pred, e1, e2):
        return (pred, e1, e2) in self.featuresList

#fb = FactBase()
#fb.addUnary("duck", "John")
#print(fb.queryUnary("duck", "John"))
#print(fb.queryUnary("duck", "Adelina"))
#print(fb.queryBinary("love", "Mary", "John")) // note that in this case e1 and e2 are not interchangable


import re
from nltk.corpus import brown
def verb_stem(s):
    #extracts the stem from the 3sg form of a verb, or returns empty string
    if (re.match("\w*([^(ch)(sh)aeiou])s$", s)):
        #  print(s[:-1])
        infinitive = s[:-1]
    elif(re.match("\w*([aeiou])ys$", s)):
        #  print(s[:-1])
        infinitive = s[:-1]
    elif (re.match("\w*([^aeiou])ies$", s) and len(s) >=5):
        #  print(s[:-3] + "y")
        infinitive = s[:-3] + "y"
    elif (re.match("[^aeiou]ies$", s)):
        #  print(s[:-1])
        infinitive = s[:-1]
    elif (re.match("\w*([(ch)(sh)(zz)(ss)ox])es$", s)):
        #  print(s[:-2])
        infinitive = s[:-2]
    elif (re.match("\w*([^s][s])es$", s) or re.match("\w*([^z][z])es$", s)):
        #  print(s[:-1])
        infinitive = s[:-1]
    elif (re.match("has", s)):
        #  print("have")
        infinitive = "have"
    elif (re.match("\w*([^(ch)(sh)iosxz])es$", s)):
        # print(s[:-1])
        infinitive = s[:-1]
    else:
        # print("")
        infinitive = ""
        #return infinitive
    
    if ((s, 'VBZ') in brown.tagged_words() and (infinitive, 'VB') in brown.tagged_words()):
        return infinitive
    else:
        return ''

#verb_stem("flys")
#verb_stem("flies")


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:  
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

