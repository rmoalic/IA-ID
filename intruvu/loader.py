import xml.etree.ElementTree as ET
from os import listdir, path
import json

def load_flows(file_name):
    """Load a list of flows from an xml file

    :param file_name: path to the xml file to load
    :returns: list of dict containing flow information"""
    flows = list()
    root = ET.parse(file_name).getroot()
    for flow in root:
        flow_dict = dict()
        for e in flow:
            try:
                flow_dict[e.tag] = int(e.text)
            except:
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


def index_files(dir_a, index_name, es, bulk_size=25000000):
    files = [path.join(dir_a, x) for x in listdir(dir_a) if ".xml" in x]
    if es.indices.exists(index_name):
        print("dropping index: {}".format(index_name))
        es.indices.delete(index=index_name)
    request_body = dict()
    request_body["settings"] = dict()
    request_body["settings"]["number_of_shards"] = 1
    request_body["settings"]["number_of_replicas"] = 0
    print("creating index: {}".format(index_name))
    es.indices.create(index=index_name, body=json.dumps(request_body))
    size = 0
    for f in files:
        print("loading file {}".format(f))
        try:
            flows = load_flows(f)
            bulk_data = list()
            for i, flw in enumerate(flows):
                op_dict = dict()
                op_dict["index"] = dict()
                op_dict["index"]["_index"] = index_name
                op_dict["index"]["_type"] = "tata"
                op_dict["index"]["_id"] = "{}-{}".format(f, i)
                json_op_dict = json.dumps(op_dict)
                json_flw = json.dumps(flw)
                message_size = len(json_op_dict) + len(json_flw)
                if size + message_size >= bulk_size:
                    print("bulk insert for {}, {} {}".format(f, i, size+1))
                    es.bulk(index=index_name, body=bulk_data, refresh=True)
                    bulk_data = list()
                    size = 0
                size = size + message_size
                bulk_data.append(json_op_dict)
                bulk_data.append(json_flw)
            print("bulk insert for {}: end".format(f))
            es.bulk(index=index_name, body=bulk_data, refresh=True)
        except MemoryError:
            print('Not enough RAM.')
        except Exception as e:
            print(e)

