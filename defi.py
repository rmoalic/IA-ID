import argparse
import sys
from collections import Counter
import numpy as np
from sklearn.preprocessing import normalize
from elasticsearch import Elasticsearch
from intruvu.flowES import FlowES
from intruvu.loader import index_files
from intruvu.ml import train_classifier

###############
## Arguments ##
###############

arg_parser = argparse.ArgumentParser(description='Intruder detection - défi', formatter_class=argparse.RawTextHelpFormatter)
arg_parser.add_argument("-r", action='store_true', required=False, help=
"""Index files to ElasticSearch and exit the program.
Files must be indexed before working with classifiers.""")
arg_parser.add_argument("--index", type=str, nargs=1, default=["defi"], required=False, help=
"""Name of the ElasticSearch index to use.
default: "flow" """)
arg_parser.add_argument("--dir_train", type=str, nargs=1, default=["./defi_train"], required=False, help=
"""Directory to load the XML training file(s) from.
This directory contain the file(s) used for the training.
It shouldn't contain any file with unknown tag.
default: "./defi_train" """)
arg_parser.add_argument("--dir_test", type=str, nargs=1, default=["./defi_test"], required=False, help=
"""Directory to load the XML test file(s) from.
This directory contain the file(s) used for the test.
default: "./defi_test" """)
arg_parser.add_argument("--output", type=str, nargs=1, default=["output.txt"], required=False, help=
"""Name of the output file containing the results.
default: "output" """)

args = arg_parser.parse_args()

###################
## ElasticSearch ##
###################

es = Elasticsearch()
print(es.info())

index_name = args.index[0]

if args.r:
    index_files(args.dir_train[0], index_name, es)
    index_files(args.dir_test[0], index_name+'_test', es)
    print('all files indexed !')
    sys.exit()

flow = FlowES(es, args.index[0])
flow_test = FlowES(es, args.index[0]+'_test')


######################
## Machine Learning ##
######################

vect_l, expected_l = flow.get_vectors_for_application("HTTPWeb")
print("classes", Counter(expected_l))

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier

classifier = KNeighborsClassifier(5)
# train_classifier(classifier, vect_l, expected_l)

print("train")
X = np.array(vect_l)
y = np.array(expected_l)
X = normalize(X)
classifier.fit(X, y)
print("end train")

vect_t, expected_t = flow_test.get_vectors_for_application("HTTPWeb")
del expected_t

print("predict")
X = np.array(vect_t)
X = normalize(X)
predictions = classifier.predict(X)
predictions_proba = classifier.predict_proba(X)
print("end predict")

with open(args.output[0], "wt") as f:
    for pred, score in zip(predictions, predictions_proba):
        f.write("{}\t{}\n".format(score[int(pred)], pred))

print("done !")