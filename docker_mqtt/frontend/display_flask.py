import nltk
import os
import sys
#sys.path.insert(1, "../utils_")

import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import pickle
from utils_.config import remove_empty_words_1, tokenize_data, remove_stop_words, stemming, lemmatization, remove_garbage, create_tf_idf, tf_idf_transform_data
import flask
from flask import Flask, request, render_template
app = Flask(__name__)
############################### ADDED  #####################################
import logging 
import datetime
script_name = 'app-flask'
############################################################################


@app.route('/')
def index():
	#line ='a bad film, am not happy to watch it'
	#response = prediction(line)
	return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
	if request.method=='POST':
		var = request.form
		response = prediction(var['chaine'])
		print(response)
		if response == 0 :
			response = '<img class="mb-4" width="72" height="72" src="https://cdn.shopify.com/s/files/1/1061/1924/products/Sad_Face_Emoji_large.png?v=1571606037"/>'
		else: 
			response = '<img class="mb-4" width="72" height="72" src="https://cdn.shopify.com/s/files/1/1061/1924/products/Emoji_Icon_-_Happy_large.png?v=1571606093"/>'
	#return render_template('result.html',result=str(response))
	return str(response)


def workflow(dataset):

	dataset = remove_empty_words_1(dataset)
	dataset = tokenize_data(dataset)
	dataset = remove_stop_words(dataset)
	dataset = stemming(dataset)
	dataset = lemmatization(dataset)
	dataset = remove_garbage(dataset)
	
	return dataset


def prediction(line):	
	data=[]
	
	data.append({"reviews": line, "labels":1})
	dataset = pd.DataFrame(data)

	dataset = workflow(dataset)
	#print("------------------ load models ------------------ ")
	tfidf = pickle.load(open("models/tfidf.pickle", "rb"))
	clf = pickle.load(open("models/LogisticRegression.pickle", "rb"))
	features = tf_idf_transform_data(tfidf, dataset) 

	elem_content = dataset.iloc[0]['reviews']
	features_element_treated = features[0]
	#print(features_element_treated)
	#print(elem_content)
	res1 = clf.predict(features_element_treated)	
	res = 'happy' if 1 in res1 else 'not happy'
	#print(res1)
	logging.info('{} - ({}) :  {}   ===> {}'.format(script_name, str(datetime.datetime.now()), str(line), str(res)))
	return res1[0]

port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__' : 
	logging.basicConfig(filename='logs/webAPP.log', level=logging.INFO)
	app.run(debug=True, host='0.0.0.0',port=port)
