#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import necessary libraries
import numpy as np
import math
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


# In[2]:


# load files with model parameters
import pickle
with open('logprior.pkl', 'rb') as f:
    logprior = pickle.load(f)
with open('loglikelihood.pkl', 'rb') as f:
    loglikelihood = pickle.load(f)


# In[3]:


# examine logprior value is correct
logprior


# In[4]:


# output loglikelihood values for words
loglikelihood


# In[5]:


# output length of loglikelihood
len(loglikelihood)


# In[7]:


import string
string.punctuation

stopword = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()

def toLowerCase(text):
    return text.lower()

def removePunctuation(text):
    return "".join([char for char in text if char not in string.punctuation])

def removeURLs(text):
    text = re.sub(r"http\S+", "", text) # replaces URLs starting with http 
    text = re.sub(r"www.\S+", "", text) # replaces URLs starting with www
    return text

def removeStopwords(text):
    return " ".join([word for word in re.split('\W+', text)
        if word not in stopword])

def performStemming(text):
     return" ".join([ps.stem(word) for word in re.split('\W+', text)])
    
def clean_review(review):
    '''
    Input:
        review: a string containing a review.
    Output:
        review_cleaned: a processed review. 

    '''
    lower_case = toLowerCase(review)
    removed_links = removeURLs(lower_case)
    removed_punct = removePunctuation(removed_links)
    removed_stopwords = removeStopwords(removed_punct)
    review_cleaned = performStemming(removed_stopwords)

    return review_cleaned

def naive_bayes_predict(review, logprior, loglikelihood):
    '''
    Params:
        review: a string
        logprior: a number
        loglikelihood: a dictionary of words mapping to numbers
    Return:
        total_prob: the sum of all the loglikelihoods of each word in the review (if found in the dictionary) + logprior (a number)

    '''
    
      # process the review to get a list of words
    word_l = clean_review(review).split()

    # initialize probability to zero
    total_prob = 0

    # add the logprior
    total_prob += logprior

    for word in word_l:

        # check if the word exists in the loglikelihood dictionary
        if word in loglikelihood:
            # add the log likelihood of that word to the probability
            total_prob += loglikelihood[word]

    if total_prob > 0:
        return 1
    else:
        return 0
    #return total_prob
    
review = input("Type in your review: ")
while review != "X":
    cleaned_review = clean_review(review)
    for word in cleaned_review.split():
        print(word + ": " + str(loglikelihood[word]))
    print("Predicted Class: ")
    prediction = naive_bayes_predict(cleaned_review, logprior, loglikelihood)
    if prediction == 0:
        print("0 (positive)")
    else:
        print("1 (negative)")
    print()
    review = input("Type in your review: ")
print("Thank you for using the program! Quitting the program...")


# In[ ]:





# In[ ]:




