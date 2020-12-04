## P_WE_ML_docker
P_WE_ML_docker: creating images of semantic models, preprocessing methods and deployment with flask

## Requirements

| Software  |
| ----------------- | 
|    flask, scikit-learn, docker, MQTT, | 

```
virtualenv --python=python3 env
source env/bin/activate
pip install -r requirements.txt
```

first of all, clone the project 
```
mkdir P_WE_ML_docker
cd P_WE_ML_docker
git init
git clone https://github.com/adlaneKadri/P_WE_ML_docker.git
```
uzip models folder
```
you find it here download it): https://drive.google.com/drive/u/1/folders/1onlP1L7H_aPQVRgHr-v5cOGpme0qs9ug
unzip P_WE_ML/models.zip
```

## How to use ?
to run the frontend 
```
cd frontend
python3 display_flask.py
> ON your browser : 
http://127.0.0.1:5000/
```

to run the preprocessing
```
cd backend/preprocessing
python3 processing.py
```

to run the word embeding
```
cd backend/bow
python3 bag_of_word.py
```
to run a machine learning model
```
cd backend/ml_hub
>choose your model (for example: decision tree)
python3 decision_tre.py
```
