import xml.etree.ElementTree as ET
from os import listdir, path


def load_flows(file_name):
    """Load a list of flows from an xml file

    :param file_name: path to the xml file to load
    :returns: list of dict containing flow information"""
    flows = list()
    root = ET.parse(file_name).getroot()
    for flow in root:
        flow_dict = dict()
        for e in flow:
            flow_dict[e.tag] = e.text
        flows.append(flow_dict)
    return flows


def load_files(dir_a, store=None):
    """
    Load flows from all xml files in a directory to a supplied shelve

    :param dir_a: directory to load files from
    :param store: a key store to load the content in | "filname" -> list(dict(), dict()) |
    :return: the store
    """
    if store is None:
        store = dict()
    files = [path.join(dir_a, x) for x in listdir(dir_a) if ".xml" in x]
    for f in files:
        if f in store:
            break
        print("loading file {}".format(f))
        try:
            flows = load_flows(f)
            store[f] = flows
        except MemoryError:
            print('Not enough RAM.')
        except Exception as e:
            print(e)
    return store
