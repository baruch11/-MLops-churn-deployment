# PURPOSE: dump the (stupid) model predicting the appetence score of a customer as a pickle file. If run, the model will train and will be saves in chaos/domain/model.pkl
# EXPLANATION: this file should not be used. It's just the source code of the pickle model for your information

import os
import pickle

import numpy as np
from sklearn.ensemble import RandomForestClassifier

import chaos


def train_model():
    """Returns the trained RandomForestClassifier model
    
    Explanation
    -----------
    This is an example taking as input 3 float features
    """
    N_FEATURES = 3
    N_ROW = 10000
    train_features = np.random.uniform(0, 1, (N_ROW, N_FEATURES))
    train_target = np.random.randint(0, 2, (N_ROW))
    rf = RandomForestClassifier(n_estimators=20)
    rf.fit(train_features, train_target)
    return rf

def dump_model(model, filename: str):
    with open(filename, 'wb') as handle:
        pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    model = train_model()
    DESTINATION_FOLDER = os.path.join(chaos.__path__[0], "domain")
    FILENAME = os.path.join(DESTINATION_FOLDER, "model.pkl")
    dump_model(model, FILENAME)
