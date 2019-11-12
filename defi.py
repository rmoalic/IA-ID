import argparse
import sys
import numpy as np
from sklearn.preprocessing import normalize
from elasticsearch import Elasticsearch
from intruvu.flowES import FlowES
from intruvu.loader import index_files
from intruvu.ml import train_classifier

###############
## Arguments ##
###############

arg_parser = argparse.ArgumentParser(description='Intruder detection - defi')
arg_parser.add_argument("--dir-train", type=str, nargs=1, default=["./defi_train"], required=False, help="directory to load the xml files from")
arg_parser.add_argument("--dir-test", type=str, nargs=1, default=["./defi_test"], required=False, help="directory to load the xml test files from")
arg_parser.add_argument("-r", action='store_true', required=False, help="reindex")
arg_parser.add_argument("--index", type=str, nargs=1, default=["flow"], required=False, help="index name")
arg_parser.add_argument("--output", type=str, nargs=1, default=["output.txt"], required=False, help="index name")

args = arg_parser.parse_args()

###################
## ElasticSearch ##
###################

es = Elasticsearch()
print(es.info())

index_name = args.index[0]

if args.r:
    index_files(args['dir-train'][0], index_name, es)
    index_files(args['dir-test'][0], index_name+'_test', es)
    print('all files indexed !')
    sys.exit()

flow = FlowES(es, args.index[0])
flow_test = FlowES(es, args.index[0]+'_test')


######################
## Machine Learning ##
######################

vect_l, expected_l = flow.get_vectors_for_application("HTTPWeb")

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier

classifier = KNeighborsClassifier()
train_classifier(classifier, vect_l, expected_l)

vect_t, expected_t = flow_test.get_vectors_for_application("HTTPWeb")
del expected_t

X = np.array(vect_l)
X = normalize(X)
predictions = classifier.predict(X)
predictions_proba = classifier.predict_proba(X)

with open(args.output[0], "wt") as f:
    for pred, score in zip(predictions, predictions_proba):
        f.write("{}\t{}\n".format(score[int(pred)], pred))

print("done !")