import numpy as np
from sklearn.preprocessing import normalize

def defi(classifier, vect_l):
    X = np.array(vect_l)
    X = normalize(X)
    predictions = classifier.predict(X)
    predictions_proba = classifier.predict_proba(X)

    for pred, score in zip(predictions, predictions_proba):
        print("{}\t{}".format(score[int(pred)], pred))