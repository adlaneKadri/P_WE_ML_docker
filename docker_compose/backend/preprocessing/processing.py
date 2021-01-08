import sys
#sys.path.insert(1, "../..")
import os
import nltk
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
from utils_.config import remove_empty_words_1, tokenize_data, remove_stop_words, stemming, lemmatization, remove_garbage
import pickle

nltk.download('wordnet')
nltk.download('stopwords')
#PATH = os.path.dirname(os.getcwd())
PATH = os.getcwd()

def load_data(positive_train_data_path, negative_train_data_path):
	#print(positive_train_data_path)
	data = []
	for file in os.listdir(positive_train_data_path):
		with open(os.path.join(positive_train_data_path + file), "r") as f:
			line = f.readlines()[0]
			data.append({"reviews": line, "labels":1})
	
	for file in os.listdir(negative_train_data_path):
		with open(os.path.join(negative_train_data_path + file), "r") as f:
			line = f.readlines()[0]
			data.append({"reviews": line, "labels":0})

	dataset = pd.DataFrame(data)
	#dataset = data
	#print(pos.head(5))
	return dataset


def training_data():

	pos_train_data_path = os.path.join(PATH, "dataset", "pos", "")
	neg_train_data_path = os.path.join(PATH, "dataset", "neg", "")
	dataset = load_data(pos_train_data_path, neg_train_data_path)

	dataset = remove_empty_words_1(dataset)
	dataset = tokenize_data(dataset)
	dataset = remove_stop_words(dataset)
	dataset = stemming(dataset)
	dataset = lemmatization(dataset)
	dataset = remove_garbage(dataset)
	return dataset

def testing_data():	
	pos_train_data_path = os.path.join(PATH, "dataset", "pos", "")
	neg_train_data_path = os.path.join(PATH, "dataset", "neg", "")
	dataset = load_data(pos_train_data_path, neg_train_data_path)
	dataset = remove_empty_words_1(dataset)
	dataset = tokenize_data(dataset)
	dataset = remove_stop_words(dataset)
	dataset = stemming(dataset)
	dataset = lemmatization(dataset)
	dataset = remove_garbage(dataset)
	return dataset

def main():
	print("------------------ data loading ---------------------")
	train_data = training_data()
	test_data = testing_data()
	
	pos_train_data_xls = os.path.join(PATH, "dataset","train_data.xlsx")
	pos_test_data_xls = os.path.join(PATH, "dataset","test_data.xlsx")
	
	train_data.to_excel(pos_train_data_xls, index = False, engine='xlsxwriter')
	test_data.to_excel(pos_test_data_xls, index = False, engine='xlsxwriter')
	
	# train_data.to_csv ("dataset/train_data.csv", index = False)
	# test_data.to_csv ("dataset/test_data.csv", index = False)


main()