import shutil
import nltk
import os
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pickle

def remove_empty_words_1(dataset):
    for i in range(dataset.shape[0]):
    	review= dataset["reviews"][i]
    	review=review.lower()
    	#review = review.translate(string.maketrans("",""), string.punctuation)
    	review = review.strip()

    	review=review.replace("<br /><br />"," ")
    	review=review.replace("<br />"," ")
    	dataset["reviews"][i] = review 
    return dataset

def tokenize_data(dataset):
    tokenizer = nltk.tokenize.TreebankWordTokenizer()
    for i in range(dataset.shape[0]):
    	dataset["reviews"][i] = tokenizer.tokenize(dataset["reviews"][i])
    return dataset

def remove_stop_words(dataset):
    stop_words = set(stopwords.words('english'))
    for i in range(dataset.shape[0]):
        dataset["reviews"][i] = ([token.lower() for token in dataset["reviews"][i] if token not in stop_words])
    
    return dataset

def stemming(dataset):
	stemmer= nltk.stem.PorterStemmer()
	for i in range(dataset.shape[0]):
		dataset.reviews[i] = ([stemmer.stem(token) for token in dataset.reviews[i]])
	return dataset

def lemmatization(dataset):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for i in range(dataset.shape[0]):
        dataset.reviews[i] = " ".join([lemmatizer.lemmatize(token) for token in dataset.reviews[i]]).strip()
    return dataset

def remove_garbage(dataset):
    garbage = "~`!@#$%^&*()_-+={[}]|\:;'<,>.?/"
    for i in range(dataset.shape[0]):

    	dataset.reviews[i] = "".join([char for char in dataset.reviews[i] if char not in garbage])
    return dataset

################################## TF IDF ############################################

def create_tf_idf(train_data, test_data):
    corpus = pd.DataFrame({"reviews": train_data["reviews"]})
    corpus.reviews.append(test_data["reviews"], ignore_index=True)
    tfidf = TfidfVectorizer(min_df=2, max_df=0.5, ngram_range=(1,2))
    tfidf.fit(corpus["reviews"])
    return tfidf

def tf_idf_transform_data(tfidf, dataset):
    features = tfidf.transform(dataset["reviews"])
    return features


################################## Bag of WORD ############################################


def create_bow(train_data, test_data):
    corpus = pd.DataFrame({"reviews": train_data["reviews"]})
    corpus.reviews.append(test_data["reviews"], ignore_index=True)
    bow = CountVectorizer(min_df=2, max_df=0.5, ngram_range=(1,2))
    bow.fit(corpus["reviews"])
    return bow

def bow_transform_data(bow, dataset):
    features = bow.transform(dataset["reviews"])
    return features

