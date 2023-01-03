import os
import chaos


def test_street_fighter():
    assert "guile" > "bison"


def test_model_file_exists():
    model = os.path.join(chaos.__path__[0], "domain/model.pkl")
    assert os.path.isfile(model)