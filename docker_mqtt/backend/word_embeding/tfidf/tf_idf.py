import sys
#sys.path.insert(1, "../..")
import os
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
from utils_.config import remove_empty_words_1, tokenize_data, remove_stop_words, stemming, lemmatization, remove_garbage, create_tf_idf, tf_idf_transform_data
import pickle
############################### ADDED  #####################################
import paho.mqtt.client as mqtt
import logging 
import datetime
logging.basicConfig(filename='logs/tfidf.log', level=logging.DEBUG)
script_name = 'TF-IDF'
finished = False
PATH = os.getcwd()

##############################  Communication Part  #################################

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("elhamdoulilah/team",2)

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if str((msg.payload).decode('utf8')) == 'preprocessing':
		worker(str(msg.payload))
		#tfidf_worker(str(msg.payload))
	else:
		print("Not my job !!!! :)")
		logging.warning('{} - ({}) : reveciving job => {}'.format(script_name,str(datetime.datetime.now()),str(msg.payload)))
#####################################################################################

def load_data():
	train_data = pd.read_excel('dataset/train_data.xlsx') 
	test_data = pd.read_excel('dataset/test_data.xlsx') 
	train_labels = train_data["labels"]  #Taking lables in separate
	test_labels = test_data["labels"]    #variables
	return train_data, test_data, train_labels, test_labels

def tfidf_worker(message):
	global finished 
	logging.info('{} - ({}) : ###################### START ########################'.format(script_name, str(datetime.datetime.now())))
	logging.debug('{} - ({}) : Loading data'.format(script_name, str(datetime.datetime.now())))
	train_data, test_data, train_labels, test_labels = load_data()

	logging.debug('{} - ({}) : creating tfidf matrix'.format(script_name, str(datetime.datetime.now())))
	tfidf = create_tf_idf(train_data, test_data)  #Fitting the vecorizer
	
	logging.debug('{} - ({}) : transforming tfidf'.format(script_name, str(datetime.datetime.now())))
	train_features = tf_idf_transform_data(tfidf, train_data)  #transforming 
	test_features = tf_idf_transform_data(tfidf, test_data)    #Train and Test
	train_labels = train_data["labels"]  #Taking lables in separate
	test_labels = test_data["labels"]    #variables
	
	logging.debug('{} - ({}) : model tfidf saved'.format(script_name, str(datetime.datetime.now())))
	#print("------------------------  saving tfidf ------------------------ ")
	pickle.dump(tfidf, open("models/tfidf.pickle", "wb"))
	pickle.dump(train_features, open("models/train_features_tfidf.pickle", "wb"))
	pickle.dump(test_features, open("models/test_features_tfidf.pickle", "wb"))
	
	finished = True
	logging.info('{} - ({}) : ###################### Finished  ########################'.format(script_name, str(datetime.datetime.now())))

def worker(message):
	tfidf_worker(message)

	try:
		client.loop_stop()
	except: 
		pass

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	#client.connect("mqtt.eclipse.org", 1883, 60)
	client.connect("broker.emqx.io", 1883, 60)
	client.loop_start() 
	client.publish("elhamdoulilah/team","tfidf")
	client.loop_stop()

def main():
	logging.info('{} - ({}) : ###################### On listing ########################'.format(script_name,str(datetime.datetime.now())))
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	#client.connect("mqtt.eclipse.org", 1883)
	client.connect("broker.emqx.io", 1883)
	#client.loop_forever()
	client.loop_start()
	while not finished: 
		#client.loop(timeout=500.0)
		pass
	client.loop_stop()

	
main()
#tfidf_worker("start")





####################################################################################