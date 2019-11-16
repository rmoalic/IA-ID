import argparse
import shelve
import random
import sys
from collections import Counter
import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch
from intruvu.flow import Flow
from intruvu.flowES import FlowES
from intruvu.loader import load_files, index_files
from intruvu.ml import train_classifier


###############
## Arguments ##
###############

arg_parser = argparse.ArgumentParser(description='Intruder detection')
# arg_parser.add_argument("--cache", type=str, nargs=1, default=["fourre-tout"], required=False, help="name of the cache file")
# arg_parser.add_argument("-e", action='store_true', required=False, help="process one file only")
arg_parser.add_argument("--dir", type=str, nargs=1, default=["./ISCX_train"], required=False, help=
"""Directory to load the XML file(s) from.
This directory contain the file(s) used for the classification.
default: "./ISCX_train" """)
arg_parser.add_argument("-r", action='store_true', required=False, help=
"""Index files to ElasticSearch and exit the program.
Files must be indexed before working with classifiers.""")
arg_parser.add_argument("--index", type=str, nargs=1, default=["flow"], required=False, help=
"""Name of the ElasticSearch index to use.
default: "flow" """)

args = arg_parser.parse_args()


############
## Shelve ##
############

#with shelve.open(FT, 'c') as ft:
#    load_files(args.dir, ft)

# ft = shelve.open(FT, 'r')
#
# if args.e:
#     flow = Flow(ft[list(ft.keys())[1]])
# else:
#flow = Flow([x for xs in ft.values() for x in xs])


###################
## ElasticSearch ##
###################

es = Elasticsearch()
print(es.info())

index_name = args.index[0]

if args.r:
    index_files(args.dir[0], index_name, es)
    print('all files indexed !')
    sys.exit()

flow = FlowES(es, index_name)

######################
## Machine Learning ##
######################

vect_l, expected_l = flow.get_vectors_for_application("HTTPWeb", limit=10000)
classes = Counter(expected_l)
print("classes", classes)
assert len(classes) >= 2, "Il faut au minimum deux classes pour classifier"

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier

classifier = KNeighborsClassifier(5)
train_classifier(classifier, vect_l, expected_l)
classifier = MultinomialNB()
train_classifier(classifier, vect_l, expected_l)
classifier = GaussianNB()
train_classifier(classifier, vect_l, expected_l)
classifier = MLPClassifier(alpha=1e-4, hidden_layer_sizes=(100,50), random_state=1)
train_classifier(classifier, vect_l, expected_l)

#######################
## Print information ##
#######################

print(flow.get_protocols())
print(list(flow.get_flows_for_protocol("igmp")))
print(flow.get_flows_count_by_protocol())
# print(flow.get_payload_by_protocol())
print(flow.get_bytes_count_by_protocol())
print(flow.get_packets_count_by_protocol())
print(flow.get_applications())
print(list(flow.get_flows_for_application("WebMediaAudio")))
# print(flow.get_payload_by_application())
print(flow.get_bytes_count_by_application())
print(flow.get_packets_count_by_application())

