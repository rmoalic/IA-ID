import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import GroupKFold
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import normalize, MinMaxScaler, StandardScaler


def stats(classifier, X, y):
    """
    Make some statistics about a prediction

    :param classifier: the classifier used for the test
    :param X: the flows vectors used for the test (list)
    :param y: the tags of the flows used for the test (list)
    :return: some metrics about the test
    """
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


def train_classifier(classifier, vect_l, expected_l, nb_group=5, normalizer=True):
    """
    Train a classifier and test it

    :param classifier: the classifier
    :param vect_l: the flows vectors for an application (list)
    :param expected_l: the tags of the flows (list)
    :param nb_group: the number of folds used for cross-validation
    :param normalizer: true to normalize data, false otherwise
    """
    name = type(classifier).__name__
    X = np.array(vect_l)
    y = np.array(expected_l)

    if normalizer:
        X = normalize(X)

    X, y = shuffle(X, y)

    group_kfold = GroupKFold(n_splits=nb_group)

    group = make_group(len(X), nb_group)

    # all_fpr = np.array([])
    # all_tpr = np.array([])
    for i, (train_index, test_index) in enumerate(group_kfold.split(X, y, group)):
        classifier.fit(X[train_index], y[train_index])

        probs = classifier.predict_proba(X[test_index])[:, 1]  # positive class proba
        fpr, tpr, thresholds = roc_curve(y[test_index], probs)
        # all_fpr = np.concatenate((all_fpr, fpr))
        # all_tpr = np.concatenate((all_tpr, tpr))
        plot_roc_curve(fpr, tpr, "{} - {}".format(name, i))
        AUC = auc(fpr, tpr)
        stats_r = stats(classifier, X[test_index], y[test_index])
        print("accuracy {:.4f} time {:4.0f}ms false_positive {:4d} false_negative {:4d} recall {:.4f} prec {:.4f} F1 {:.4f} AUC {:.4f} name {}-{}".format(*stats_r, AUC, name, i))
    # plot_roc_curve(all_fpr, all_tpr, "mean {}".format(name))


def plot_roc_curve(fpr, tpr, name):
    """
    Draw a roc curve

    :param fpr: false positives rates (array)
    :param tpr: true positives rates (array)
    :param name: diagram name
    """
    plt.plot(fpr, tpr, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC {}'.format(name))
    plt.legend()
    plt.show()


def make_group(n, part):
    """
    Create a list containing n elements, with different parts of equal sizes
    if n isn't dividable by part, the result is padded with 0's

    >>> make_group(9, 3)
    array([0, 0, 0, 1, 1, 1, 2, 2, 2])

    >>> make_group(9, 2)
    array([0, 0, 0, 0, 1, 1, 1, 1, 0])

    :param n: number of elements
    :param part: numbers of parts to create
    :return: an array
    """
    ret = list()
    group_size = n // part
    for i in range(part):
        ret.extend([i for j in range(group_size)])
    reste = n % part
    if reste > 0:
        ret.extend([0 for i in range(reste)])
    assert len(ret) == n
    return np.array(ret)