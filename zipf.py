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
arg_parser.add_argument("--dir", type=str, nargs=1, default=["./ISCX_train"], required=False, help="directory to load the xml files from")
arg_parser.add_argument("-r", action='store_true', required=False, help="reindex")
arg_parser.add_argument("--index", type=str, nargs=1, default=["flow"], required=False, help="index name")

args = arg_parser.parse_args()

###################
## ElasticSearch ##
###################

es = Elasticsearch()
print(es.info())

index_name = args.index[0]

if args.r:
    index_files(args.dir[0], index_name, es)

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
