
import os
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
############################### ADDED  #####################################
import paho.mqtt.client as mqtt
import logging 
import datetime
logging.basicConfig(filename='logs/logisticRegression.log', level=logging.DEBUG)
############################################################################
# nltk.download('wordnet')
# nltk.download('stopwords')
PATH = os.getcwd()


script_name = 'LOGISTIC REGRESSION'
finished = False
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

def lr_worker(message):
	global finished
	logging.info('{} - ({}) : ###################### START ########################'.format(script_name,str(datetime.datetime.now())))
	logging.debug('{} - ({}) : Loading data'.format(script_name,str(datetime.datetime.now())))
	train_data, test_data, train_labels, test_labels = load_data()

	logging.debug('{} - ({}) : load encoding models'.format(script_name,str(datetime.datetime.now())))
	#print("------------------ load encoding models ------------------ ")
	tfidf, train_features, test_features = load_encoding_model()
	
	logging.debug('{} - ({}) : LG model training'.format(script_name,str(datetime.datetime.now())))
	#print("------------------      LG model      -------------------- ")
	clf = LogisticRegression(random_state=0, solver='lbfgs')
	clf.fit(train_features, train_labels)
	score = clf.score(test_features, test_labels)
	logging.debug('{} - ({}) :  model saved with score {}%'.format(script_name,str(datetime.datetime.now()), score*100))
	#print("score is : {}%".format(score*100))
	pickle.dump(clf, open("models/LogisticRegression.pickle", "wb"))
	##############################################################
	#client.loop_stop()
	logging.info('{} - ({}) : ###################### Finished  ########################'.format(script_name,str(datetime.datetime.now())))
	finished = True


#main()


##############################  Communication Part  #################################

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("elhamdoulilah/team",2)

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if str((msg.payload).decode('utf8')) == 'tfidf':
		lr_worker(str(msg.payload))
	else:
		print("Not my job !!!! :)")
		logging.warning('{} - ({}) : reveciving strange job => {}'.format(script_name,str(datetime.datetime.now()),str(msg.payload)))

logging.info('{} - ({}) : ###################### On listing ########################'.format(script_name,str(datetime.datetime.now())))
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


#while True:
#client.connect("mqtt.eclipse.org", 1883)
client.connect("broker.emqx.io", 1883)
#client.loop_forever()
client.loop_start()
while not finished: 
	#client.loop(timeout=500.0)
	pass
client.loop_stop()
####################################################################################