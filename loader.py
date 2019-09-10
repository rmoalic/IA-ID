import xml.etree.ElementTree as ET
from os import listdir, path
import shelve

FT = "fourre-tout"

def load_flows(file_name):
    flows = list()

    root = ET.parse(file_name).getroot()

    for flow in root:
        flow_dict = dict()
        for e in flow:
            flow_dict[e.tag] = e.text
        flows.append(flow_dict)
    return flows

def load_files(dirA):
    files = [path.join(dirA,x) for x in listdir(dirA) if ".xml" in x]
    with shelve.open(FT) as ft:
        for f in files:
            print("loading file {}".format(f))
            try:
                flows = load_flows(f)
                ft[f] = flows
            except e:
                print(e)

if not path.isfile(FT):
    load_files('./ISCX_train')

with shelve.open(FT) as ft:
   print(list(ft.keys()))
