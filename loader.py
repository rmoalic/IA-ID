import xml.etree.ElementTree as ET
from os import listdir, path
import shelve

FT = "fourre-tout"


def load_flows(file_name):
    """Load a list of flows from an xml file"""
    flows = list()
    root = ET.parse(file_name).getroot()
    for flow in root:
        flow_dict = dict()
        for e in flow:
            flow_dict[e.tag] = e.text
        flows.append(flow_dict)
    return flows


def load_files(dir_a):
    """Load flows from all xml files in a directory"""
    files = [path.join(dir_a, x) for x in listdir(dir_a) if ".xml" in x]
    with shelve.open(FT) as f_t:
        for f in files:
            print("loading file {}".format(f))
            try:
                flows = load_flows(f)
                f_t[f] = flows
            except MemoryError:
                print('Not enough RAM.')
            except Exception as e:
                print(e)


if not path.isfile(FT):
    load_files('./ISCX_train')

with shelve.open(FT) as ft:
    print(list(ft.keys()))
