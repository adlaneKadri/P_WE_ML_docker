
import os
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import pickle
from sklearn.ensemble import GradientBoostingClassifier
############################### ADDED  #####################################
import logging 
import datetime
logging.basicConfig(filename='logs/gradientBoosting.log', level=logging.DEBUG)
script_name = 'gradient-boosting'
############################################################################
# nltk.download('wordnet')
# nltk.download('stopwords')
PATH = os.getcwd()



def load_data():
	train_data = pd.read_excel('dataset/train_data.xlsx') 
	test_data = pd.read_excel('dataset/test_data.xlsx') 
	train_labels = train_data["labels"]  #Taking lables in separate
	test_labels = test_data["labels"]    #variables
	return train_data, test_data, train_labels, test_labels

def load_encoding_model():
	tfidf = pickle.load(open("models/tfidf.pickle", "rb"))
	train_features = pickle.load(open("models/train_features.pickle", "rb"))
	test_features = pickle.load(open("models/test_features.pickle", "rb"))	
	return tfidf, train_features, test_features

def main():
	logging.info('{} - ({}) : ###################### START ########################'.format(script_name,str(datetime.datetime.now())))
	logging.debug('{} - ({}) : Loading data'.format(script_name,str(datetime.datetime.now())))
	#print("------------------     load data     --------------------- ")
	train_data, test_data, train_labels, test_labels = load_data()

	#print("------------------ load encoding models ------------------ ")
	logging.debug('{} - ({}) : load encoding models'.format(script_name,str(datetime.datetime.now())))
	tfidf, train_features, test_features = load_encoding_model()
	
	logging.debug('{} - ({}) : GB model training'.format(script_name,str(datetime.datetime.now())))
	#print("------------------      GB model      -------------------- ")
	clf = GradientBoostingClassifier(random_state=0)
	clf.fit(train_features, train_labels)
	score = clf.score(test_features, test_labels)
	#print("score is : {}%".format(score*100))
	logging.debug('{} - ({}) :  model saved with score {}%'.format(script_name,str(datetime.datetime.now()), score*100))
	pickle.dump(clf, open("models/GradientBoosting.pickle", "wb"))
	logging.info('{} - ({}) : ###################### Finished  ########################'.format(script_name,str(datetime.datetime.now())))



main()