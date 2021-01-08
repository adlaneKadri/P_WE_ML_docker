import sys
#sys.path.insert(1, "../..")
import os
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
from utils_.config import remove_empty_words_1, tokenize_data, remove_stop_words, stemming, lemmatization, remove_garbage, create_tf_idf, tf_idf_transform_data
import pickle

PATH = os.getcwd()


def load_data():
	train_data = pd.read_excel('dataset/train_data.xlsx') 
	test_data = pd.read_excel('dataset/test_data.xlsx') 
	train_labels = train_data["labels"]  #Taking lables in separate
	test_labels = test_data["labels"]    #variables
	return train_data, test_data, train_labels, test_labels

def main():
	print("------------------------  load data  --------------------------- ")
	train_data, test_data, train_labels, test_labels = load_data()


	print("------------------------ creating tfidf ------------------------ ")
	tfidf = create_tf_idf(train_data, test_data)  #Fitting the vecorizer
	
	print("------------------------ transforme tfidf ------------------------ ")
	train_features = tf_idf_transform_data(tfidf, train_data)  #transforming 
	test_features = tf_idf_transform_data(tfidf, test_data)    #Train and Test
	train_labels = train_data["labels"]  #Taking lables in separate
	test_labels = test_data["labels"]    #variables
	
	print("------------------------  saving tfidf ------------------------ ")
	pickle.dump(tfidf, open("models/tfidf.pickle", "wb"))
	pickle.dump(train_features, open("models/train_features_tfidf.pickle", "wb"))
	pickle.dump(test_features, open("models/test_features_tfidf.pickle", "wb"))


main()
