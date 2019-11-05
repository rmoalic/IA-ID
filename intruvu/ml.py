import time
from sklearn import metrics

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


def partition(data, n):
    return [data[i::n] for i in range(n)]