import requests

from chaos.infrastructure.config.config import config

api = config["api"]
host = api["host"]
port = api["port"]


def test_example1():
    endpoint = "example"    
    url = f"http://{host}:{port}/{endpoint}"
    headers = {"Content-type": "application/json"}

    data = {"question": 2}

    response = requests.get(url=url, json=data, headers=headers)
    results = response.json()
    
    assert results["answer"] == data["question"]*2


def test_example2():
    endpoint = "example"    
    url = f"http://{host}:{port}/{endpoint}"
    headers = {"Content-type": "application/json"}

    data = {"question": "a"}

    response = requests.get(url=url, json=data, headers=headers)
    results = response.json()
    
    assert results["answer"] == 0


def test_example3():
    endpoint = "example"    
    url = f"http://{host}:{port}/{endpoint}"
    headers = {"Content-type": "application/json"}

    data = {"wrong_field": "a"}

    response = requests.get(url=url, json=data, headers=headers)
    results = response.json()
    
    assert results["answer"] == 0