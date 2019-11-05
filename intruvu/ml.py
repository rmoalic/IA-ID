import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import GroupKFold
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve

def stats(classifier, X, y):
    assert len(X) == len(y)
    start_time = time.time()
    size = len(X)
    false_positive = 0
    false_negative = 0
    error = 0
    pred = list()
    for test, attended_result in zip(X, y):
        result = bool(classifier.predict([test]))
        pred.append(result)
        attended_result = bool(attended_result)
        if result != attended_result:
            error = error + 1
            if not result and attended_result:
                false_negative = false_negative + 1
            else:
                false_positive = false_positive + 1
    accuracy = 1 - (error / size)
    end_time = time.time()
    assert error == false_negative + false_positive

    F1 = metrics.f1_score(y, pred, average='macro')
    PREC = metrics.precision_score(y, pred, average='macro')
    REC = metrics.recall_score(y, pred, average='macro')

    return accuracy, (end_time - start_time) * 1000, false_positive, false_negative, REC, PREC, F1


def train_classifier(classifier, vect_l, expected_l, nb_group=5):
    X = np.array(vect_l)
    y = np.array(expected_l)

    X, y = shuffle(X, y)

    group_kfold = GroupKFold(n_splits=5)

    group = make_group(len(X), 5)

    for train_index, test_index in group_kfold.split(X, y, group):
        classifier.fit(X[train_index], y[train_index])

        probs = classifier.predict_proba(X[test_index])[:, 1]  # positive class proba
        fpr, tpr, thresholds = roc_curve(y[test_index], probs)
        plot_roc_curve(fpr, tpr, type(classifier).__name__)

        stats_r = stats(classifier, X[test_index], y[test_index])
        print("accuracy {:.4f} time {:4.0f}ms false_positive {:4d} false_negative {:4d} recall {:.4f} prec {:.4f} F1 {:.4f}".format(*stats_r))


def plot_roc_curve(fpr, tpr, name):
    plt.plot(fpr, tpr, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC {}'.format(name))
    plt.legend()
    plt.show()


def make_group(n, part):
    ret = list()
    group_size = n // part
    for i in range(part):
        ret.extend([i for j in range(group_size)])
    reste = n % part
    if reste > 0:
        ret.extend([0 for i in range(reste)])
    return np.array(ret)


def partition(data, n):
    return [data[i::n] for i in range(n)]