
import os
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import pickle
from sklearn.neural_network import MLPClassifier

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
	print("------------------     load data     --------------------- ")
	train_data, test_data, train_labels, test_labels = load_data()

	print("------------------ load encoding models ------------------ ")
	tfidf, train_features, test_features = load_encoding_model()
	
	print("------------------      MLP model      -------------------- ")
	clf = MLPClassifier(random_state=1, max_iter=300)
	clf.fit(train_features, train_labels)
	score = clf.score(test_features, test_labels)
	print("score is : {}%".format(score*100))
	pickle.dump(clf, open("models/mlp.pickle", "wb"))



main()