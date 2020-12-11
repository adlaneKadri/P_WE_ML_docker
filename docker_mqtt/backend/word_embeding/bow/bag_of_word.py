import sys
#sys.path.insert(1, "../..")
import os
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
from utils_.config import remove_empty_words_1, tokenize_data, remove_stop_words, stemming, lemmatization, remove_garbage, create_bow, bow_transform_data
import pickle
############################### ADDED  #####################################
import logging 
import datetime
logging.basicConfig(filename='logs/bag_of_words.log', level=logging.DEBUG)
script_name = 'Bag-Of-Words'
############################################################################
PATH = os.getcwd()


def load_data():
	train_data = pd.read_excel('dataset/train_data.xlsx') 
	test_data = pd.read_excel('dataset/test_data.xlsx') 
	train_labels = train_data["labels"]  #Taking lables in separate
	test_labels = test_data["labels"]    #variables
	return train_data, test_data, train_labels, test_labels

def main():
	logging.info('{} - ({}) : ###################### START ########################'.format(script_name, str(datetime.datetime.now())))
	logging.debug('{} - ({}) : Loading data'.format(script_name, str(datetime.datetime.now())))
	#print("------------------------  load data  --------------------------- ")
	train_data, test_data, train_labels, test_labels = load_data()

	logging.debug('{} - ({}) : creating BOW matrix'.format(script_name, str(datetime.datetime.now())))
	#print("------------------------ creating BOW ------------------------ ")
	bow = create_bow(train_data, test_data)  #Fitting the vecorizer
	
	logging.debug('{} - ({}) : transforming BOW'.format(script_name, str(datetime.datetime.now())))
	#print("------------------------ transforme BOW ------------------------ ")
	train_features = bow_transform_data(bow, train_data)  #transforming 
	test_features = bow_transform_data(bow, test_data)    #Train and Test
	train_labels = train_data["labels"]  #Taking lables in separate
	test_labels = test_data["labels"]    #variables

	logging.debug('{} - ({}) : model BOW saved'.format(script_name, str(datetime.datetime.now())))
	#print("------------------------  saving BOG ------------------------ ")
	pickle.dump(bow, open("models/bow.pickle", "wb"))
	pickle.dump(train_features, open("models/train_features_bow.pickle", "wb"))
	pickle.dump(test_features, open("models/test_features_bow.pickle", "wb"))
	logging.info('{} - ({}) : ###################### Finished  ########################'.format(script_name, str(datetime.datetime.now())))

main()
