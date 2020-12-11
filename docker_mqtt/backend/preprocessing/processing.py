import sys
#sys.path.insert(1, "../..")
import os
import nltk
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
from utils_.config import remove_empty_words_1, tokenize_data, remove_stop_words, stemming, lemmatization, remove_garbage
import pickle
import xlsxwriter

############################### ADDED  #####################################
import logging 
import datetime
logging.basicConfig(filename='logs/processing.log', level=logging.DEBUG)
script_name = 'PROCCESING'
############################################################################
nltk.download('wordnet')
nltk.download('stopwords')
#PATH = os.path.dirname(os.getcwd())
PATH = os.getcwd()


def load_data(positive_train_data_path, negative_train_data_path):
	#print(positive_train_data_path)
	logging.debug('{} - ({}) :  start loading data'.format(script_name, str(datetime.datetime.now())))
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
	logging.debug('{} - ({}) :  {} is loaded'.format(str(datetime.datetime.now()),script_name,  dataset.reviews.count()))
	return dataset


def training_data():
	logging.debug('{} - ({})  processing training data started'.format(script_name, str(datetime.datetime.now())))
	pos_train_data_path = os.path.join(PATH, "dataset", "pos", "")
	neg_train_data_path = os.path.join(PATH, "dataset", "neg", "")
	dataset = load_data(pos_train_data_path, neg_train_data_path)

	dataset = remove_empty_words_1(dataset)
	dataset = tokenize_data(dataset)
	dataset = remove_stop_words(dataset)
	dataset = stemming(dataset)
	dataset = lemmatization(dataset)
	dataset = remove_garbage(dataset)
	logging.debug('{} - ({})  processing training data finished'.format(script_name, str(datetime.datetime.now())))
	return dataset

def testing_data():	
	logging.debug('{} - ({})  processing testing data started'.format(script_name, str(datetime.datetime.now())))
	pos_train_data_path = os.path.join(PATH, "dataset", "pos", "")
	neg_train_data_path = os.path.join(PATH, "dataset", "neg", "")
	dataset = load_data(pos_train_data_path, neg_train_data_path)
	dataset = remove_empty_words_1(dataset)
	dataset = tokenize_data(dataset)
	dataset = remove_stop_words(dataset)
	dataset = stemming(dataset)
	dataset = lemmatization(dataset)
	dataset = remove_garbage(dataset)
	logging.debug('{} - ({})  processing training data finished'.format(script_name, str(datetime.datetime.now())))
	return dataset



############################ Communication Part ################################
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("elhamdoulilah/team",2)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

################################################################


def main():
	#print("------------------ data loading ---------------------")
	logging.info('{} - ({}) : ###################### START  ########################'.format(script_name, str(datetime.datetime.now())))
	train_data = training_data()
	test_data = testing_data()
	
	pos_train_data_xls = os.path.join(PATH, "dataset","train_data.xlsx")
	pos_test_data_xls = os.path.join(PATH, "dataset","test_data.xlsx")
	
	train_data.to_excel(pos_train_data_xls, index = False, engine='xlsxwriter')
	test_data.to_excel(pos_test_data_xls, index = False, engine='xlsxwriter')
	
	# train_data.to_csv ("dataset/train_data.csv", index = False)
	# test_data.to_csv ("dataset/test_data.csv", index = False)
	#for i in range(4000)
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	#client.connect("mqtt.eclipse.org", 1883, 60)
	client.connect("broker.emqx.io", 1883)
	client.loop_start() #loop_forever()
	client.publish("elhamdoulilah/team","preprocessing")
	client.loop_stop()
	logging.info('{} - ({}) : ###################### Finished  ########################'.format(script_name, str(datetime.datetime.now())))

main()


