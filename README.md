## P_WE_ML_docker
P_WE_ML_docker: creating images of semantic models, preprocessing methods and deployment with flask

## Requirements

``pipreqs`` - Generate requirements.txt file for any project based on imports

#### Installation
------------
    pip install pipreqs

#### Usage
-----
    pipreqs /home/project/location
    Successfully saved requirements file in /home/project/location/requirements.txt

###### requirements  content example : 
----- 
```
  nltk==3.4.5
  pandas==1.0.1
  Flask==1.1.1
  scikit_learn==0.23.2
  numpy==1.13.3
```
###### (PS: if the requirements.txt exits, you have to delete it before) [learn more](https://pypi.org/project/pipreqs/)

| Software  |
| ----------------- | 
|    flask, scikit-learn, docker, MQTT, pandas, numpy, nltk | 

```
virtualenv --python=python3 env
source env/bin/activate
pip install -r requirements.txt
```

## first of all, clone the project 
```
cd 
mkdir docker_project
cd docker_project
git init 
git clone https://github.com/adlaneKadri/P_WE_ML_docker.git
cd P_WE_ML_docker
```
you find models folder [here](https://drive.google.com/drive/u/1/folders/1onlP1L7H_aPQVRgHr-v5cOGpme0qs9ug), and download it 
uzip models folder
```

unzip P_WE_ML/models.zip
```
## Tree
```
P_WE_ML_docker
          ├── P_WE_ML
          │   └── frontend
          |   └── backend
          |       └── dataset
          |       └── ml_hub
          |           └── decision_tree/
          |           └── gradient_boosting/
          |           └── mlp/
          |           └── random_forest/
          |       └── preprocessing
          |           └── processing.py
          |       └── word_embeding
          |           └── bow/
          |           └── tfidf/
          |   └── utils_
          |       └── config.py
          |   └── models
          |   └── logs
          ├── docker
          ├── docker-compse
          ├── P_WE_ML_docker
          └── Vagrantfile
```
## How to use ?
#### P_WE_ML part
to run the frontend 
```
cd frontend
python3 display_flask.py
```
> ON your browser : 
```
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


#### dockerization of the project P_WE_ML
> PS --> volumes:  use absolute path (-v all path of your folder)

Web application 
```
cd frontend
sudo docker build -t web:1.0.0 . 

sudo docker run -v /mypath_to_docker_project/P_WE_ML_docker/docker/models:/app/models -v /mypath_to_docker_project/P_WE_ML_docker/docker/utils_:/app/utils_ -p 5000:5000 web:1.0.0
```
> ON your browser : 
```
http://0.0.0.0:5000/
```

Data preprocessing
```
cd backend/preprocessing

sudo docker build -t processing:v1 . 

sudo docker run -v /mypath_to_docker_project/P_WE_ML_docker/docker/backend/dataset:/app/dataset -v /mypath_to_docker_project/P_WE_ML_docker/docker/utils_:/app/utils_  processing:v1
```

Word embeding (for example tfidf)
```
cd backend/tfidf
sudo docker build -t tfidf:v1 . 

sudo docker run -v /mypath_to_docker_project/P_WE_ML_docker/docker/backend/dataset:/app/dataset -v /mypath_to_docker_project/P_WE_ML_docker/docker/models:/app/models  -v /mypath_to_docker_project/P_WE_ML_docker/docker/utils_:/app/utils_  tfidf:v1
```

Machine learning model (for example decision tree)
```
cd backend/ml_hub/decision_tree

sudo docker build -t decision_tree:v1 . 

sudo docker run -v /mypath_to_docker_project/P_WE_ML_docker/docker/backend/dataset:/app/dataset -v /mypath_to_docker_project/P_WE_ML_docker/docker/models:/app/models  -v /mypath_to_docker_project/P_WE_ML_docker/docker/utils_:/app/utils_  decision_tree:v1
```


#### Version with MQTT
- please create 2 folders (logs, models) 
```
mkdir /mypath_to_docker_project/P_WE_ML_docker/docker/logs
mkdir /mypath_to_docker_project/P_WE_ML_docker/docker/models
```
Web application 
```
cd frontend
sudo docker build -t web:1.0.0 . 

sudo docker run -v /mypath_to_docker_project/P_WE_ML_docker/docker/models:/app/models -v /mypath_to_docker_project/P_WE_ML_docker/docker/utils_:/app/utils_   -v  /mypath_to_docker_project/logs:/app/logs -p 5000:5000 web:1.0.0
```
> ON your browser : 
```
http://0.0.0.0:5000/
```

Data preprocessing
```
cd backend/preprocessing

sudo docker build -t processing:v1 . 

sudo docker run -v /mypath_to_docker_project/backend/dataset:/app/dataset -v /mypath_to_docker_project/utils_:/app/utils_  -v  /mypath_to_docker_project/logs:/app/logs processing:v1
```

Word embeding (for example tfidf)
```
cd backend/tfidf
sudo docker build -t tfidf:v1 . 

sudo docker run -v /mypath_to_docker_project/backend/dataset:/app/dataset -v /mypath_to_docker_project/models:/app/models  -v /mypath_to_docker_project/utils_:/app/utils_  -v  /mypath_to_docker_project/logs:/app/logs tfidf:v1
```

Machine learning model (for example logistic Regrission)
```
cd backend/ml_hub/logistic_regrission

sudo docker build -t logisticRegrission:v1 . 

sudo docker run -v /mypath_to_docker_project/backend/dataset:/app/dataset -v /mypath_to_docker_project/models:/app/models  -v /mypath_to_docker_project/utils_:/app/utils_  -v  /mypath_to_docker_project/logs:/app/logs  logisticRegrission:v1
```

#### Vagrant 
To run vagrant  (we are using ubuntu20 version in Vagrantfile configuration)
```
vagrant up
```
To destroy the current machine with all params 
```
vagrant destroy
```
To access in VM with ssh 
```
vagrant ssh
```
