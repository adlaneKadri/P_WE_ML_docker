import nltk
import os
import sys
sys.path.insert(1, "../backend")

import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import pickle
from all_functions.config import remove_empty_words_1, tokenize_data, remove_stop_words, stemming, lemmatization, remove_garbage, create_tf_idf, tf_idf_transform_data
import flask
from flask import Flask, request, render_template
app = Flask(__name__)


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
	
	#train_features = pickle.load(open("models/train_features.pickle", "rb"))
	#test_features = pickle.load(open("models/test_features.pickle", "rb"))	

	dataset = workflow(dataset)
	#print("------------------ load models ------------------ ")
	tfidf = pickle.load(open("../models/tfidf.pickle", "rb"))
	clf = pickle.load(open("../models/LogisticRegression.pickle", "rb"))
	features = tf_idf_transform_data(tfidf, dataset) 

	elem_content = dataset.iloc[0]['reviews']
	features_element_treated = features[0]
	#print(features_element_treated)
	#print(elem_content)
	res1 = clf.predict(features_element_treated)	
	#res = 'happy' if 1 in res1 else 'not happy'
	#print(res1)
	return res1[0]


if __name__ == '__main__' : 
	app.run(debug=True)
