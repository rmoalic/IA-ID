import argparse
import shelve
import random
import sys
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

##############
## Zipf law ##
##############

per = flow.get_flows_per_packet()
plt.loglog(*zip(*sorted(per.items())), linestyle='None', marker=".")
plt.xlabel("packet/flow")
plt.ylabel("flows")
plt.show()

print("done !")
