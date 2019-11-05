import argparse
import shelve
import random
import sys
import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch
from intruvu.flow import Flow
from intruvu.flowES import FlowES
from intruvu.loader import load_files, index_files
from intruvu.ml import partition, stats

arg_parser = argparse.ArgumentParser(description='Intruder detection')
arg_parser.add_argument("--cache", type=str, nargs=1, default="fourre-tout", required=False, help="name of the cache file")
arg_parser.add_argument("--dir", type=str, nargs=1, default="./ISCX_train", required=False, help="directory to load the xml files from")
arg_parser.add_argument("-e", action='store_true', required=False, help="process one file only")
arg_parser.add_argument("-r", action='store_true', required=False, help="reindex")

args = arg_parser.parse_args()

FT = args.cache

es = Elasticsearch()
print(es.info())

if args.r:
    index_files(args.dir, "flow", es)

flow = FlowES(es, "flow")
#with shelve.open(FT, 'c') as ft:
#    load_files(args.dir, ft)

ft = shelve.open(FT, 'r')
#
# if args.e:
#     flow = Flow(ft[list(ft.keys())[1]])
# else:
#flow = Flow([x for xs in ft.values() for x in xs])
#
# per = flow.get_flows_per_packet()
# plt.loglog(*zip(*sorted(per.items())), linestyle='None', marker=".")
# plt.xlabel("packet/flow")
# plt.ylabel("flows")
# plt.show()

def make_group(n, part):
    ret = list()
    group_size = n // part
    for i in range(part):
        ret.extend([i for j in range(group_size)])
    reste = n % part
    if reste > 0:
        ret.extend([0 for i in range(reste)])
    return np.array(ret)

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GroupKFold
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve

vect_l, expected_l = flow.get_vectors_for_application("SMTP")

X = np.array(vect_l)
y = np.array(expected_l)

X, y = shuffle(X, y)

group_kfold = GroupKFold(n_splits=5)

group = make_group(len(X), 5)

def plot_roc_curve(fpr, tpr, name):
    plt.plot(fpr, tpr, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC {}'.format(name))
    plt.legend()
    plt.show()

for train_index, test_index in group_kfold.split(X, y, group):
    neigh = MLPClassifier(solver="adam")
    neigh.fit(X[train_index], y[train_index])

    probs = neigh.predict_proba(X[test_index])[:, 1] # positive class proba
    fpr, tpr, thresholds = roc_curve(y[test_index], probs)
    plot_roc_curve(fpr, tpr, type(neigh).__name__)

    stats_r = stats(neigh, X[test_index], y[test_index])
    print("accuracy {:.4f} time {:4.0f}ms false_positive {:4d} false_negative {:4d} recall {:.4f} prec {:.4f} F1 {:.4f}".format(*stats_r))




sys.exit()

print(flow.get_protocols())
# print(flow.get_flows_for_protocol("igmp"))
# print(flow.get_flows_count_by_protocol())
# print(flow.get_payload_by_protocol())
print(flow.get_bytes_count_by_protocol())
print(flow.get_packets_count_by_protocol())
print(flow.get_applications())
print(flow.get_flows_for_application("WebMediaAudio"))
# print(flow.get_payload_by_application())
print(flow.get_bytes_count_by_application())
print(flow.get_packets_count_by_application())
#
# ft.close()
