# Chaos

<p align="center">
    <img src="images/churn.png" 
        width="500" 
        height="250"  />
</p>

> **The current project aims to deploy a churn detection machine learning model** into **production environment**, using some **cloud technologies** such as **Docker** and **Kubernetes**.
>
> **Original code base for churn detection model is here** :
>
> https://gitlab.com/yotta-academy/mle-bootcamp/projects/ml-project/project-1-fall-2022/churn-modelling-salima-charles-emeric


## Getting started

### Install

```
poetry config --local virtualenvs.in-project true
poetry install
```

### Run api locally

```
source .venv/bin/activate
make run-server
```
Try the api at adress http://0.0.0.0:8000/docs

## Docker image 
If you want to containerize locally your code and run it you can do the following :

### build and run:
Make sure your **GOOGLE_APPLICATION_CREDENTIALS** is set before runing image.
```
export GOOGLE_APPLICATION_CREDENTIALS=<path to json of the service account private key>
export SSH_PRIVATE_KEY=<path_to_shh_key> # Gitlab ssh key needed to import churn repo
make containerize-and-start-app
```
This command will build an image of your application, the tag of the image will be the short git sha1. It will create a local postgres sql bdd and the app will request on it. **Don't forget to add the csv data if this is the first time**

### run all tests:
The following command will enable you to build all the required environment to run unit tests, and functional tests.
Functional tests are very important because they enable you to try your application working on real elements. (Real bdd, real model etc)
In order to preserve production bdd performance, we build a local database (Postgres SQL) with docker. So don't forget to add the csv data!!. 
```
export GOOGLE_APPLICATION_CREDENTIALS=<path to json of the service account private key>
export SSH_PRIVATE_KEY=<path_to_shh_key> # Gitlab ssh key needed to import churn repo
make containerize-and-run-tests
```

### Build the app:
Exactly the same than build and run, but it don't run. 
```
export GOOGLE_APPLICATION_CREDENTIALS=<path to json of the service account private key>
export SSH_PRIVATE_KEY=<path_to_shh_key> # Gitlab ssh key needed to import churn repo
make build-docker-image
```

### Push your image in google container registry:
If you want to push your generated image directly to Google Container Registry without working with CI-CD, this is possible. 
Simply do :
```
export SHORT_SHA=$(git rev-parse --short=8 HEAD)
docker push eu.gcr.io/coyotta-2022/chaos-1:$SHORT_SHA
```


## Kubernetes

### create secret

```
kubectl create secret generic chaos-secrets-1 --from-file=key.json=<path to json of the service account private key> --from-file=<path to the config.yml>
```

## CI/CD

### Gitlab variables
	
- BASE64_GOOGLE_CREDENTIALS: (unused) base64 service account
- CONFIG_YML: yaml file with many config variables for Gitlab environment 
- GCP_SA_KEY: GCP service account private key (used to access gcp registry 
	and kubernetes)
- SSH_CHURN_ACCESS: private ssh key for churn model gitlab repo

## PROXY

help to connect to proxy

[proxy commands](proxy/proxy_SQL_connexion.md)


## GCLOUD :
help to work with gcloud.
### Identify gcloud  storage locally :
```
gcloud auth application-default login
```

🚩 **Do not forget to update your configuration files** 🚩

`config.yml` in sub folder `infrastructure/config`

```
gcs:
  bucket: "chaos-1"
  blob: "model/ChurnModelFinal.pkl"
```

## BDD
### How to work with psql commands. 
**psql commands are quite specifics** : 
#### Get help.
- `\?`
#### List databases.
- `\l`
#### List tables.
- `\dp`

### Local installation :
In order to not affect production data, in local environments we will work with a postgres container emulating bdd. 
We need to build and launch the containers, and to add data to it.

#### Run postgres bdd :
First don't forget previous export : 
```export GOOGLE_APPLICATION_CREDENTIALS=./proxy/gcp_key.json```
And then launch bdd container only !!
```make containerize-and-start-bdd```
#### Insert test csv data into postgres database: 
If this is the first time you create locally this bdd, you need to insert csv data to play with.
In a new shell,launch the following code : 
(PS : if you want to give custom test_sample_customer and test_sample_indicators filepath, you can use the "-c" and "-i" options of this util.)

```
python3 utils/postgres_manager.py
```

After this operation don't forget to kill the previous shell with db running, and then you can build and launch your app, or launch unit and functional tests. See the section Docker : build and run, or run all tests.