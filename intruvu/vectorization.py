from murmurhash import hash
import re

def direction_converter(direction):
    ret = 0
    if direction == "L2R":
        ret = 1
    elif direction == "R2L":
        ret = 2
    elif direction == "L2L":
        ret = 3
    elif direction == "R2R":
        ret = 4
    return ret


def payload_hist(data):
    array = {chr(x): 0 for x in range(255)}
    if data is None:
        return array.values()
    ascii_data = list(re.sub("[^\x00-\x7f]", "", data))
    for d in ascii_data:
        array[d] = array[d] + 1
    assert len(array) == 255
    return array.values()


def insert_numerical_values(flow):
    flow["appName_n"] = hash(flow["appName"])
    flow["protocolName_n"] = hash(flow["protocolName"])
    flow["source_n"] = tuple([int(e) for e in flow["source"].split('.')])
    flow["destination_n"] = tuple([int(e) for e in flow["destination"].split('.')])
    flow["direction_n"] = direction_converter(flow["direction"])
    flow["sourcePayloadAsUTF_n"] = tuple(payload_hist(flow.get("sourcePayloadAsUTF", None)))
    flow["destinationPayloadAsUTF_n"] = tuple(payload_hist(flow.get("destinationPayloadAsUTF", None)))

def make_vector(flow):
    return (flow.get("totalSourceBytes", None),
            flow.get("totalDestinationBytes", None),
            flow.get("totalSourcePackets", None),
            flow.get("totalDestinationPackets", None),
            flow.get("source_n", None),
            flow.get("destination_n", None),
            flow.get("direction_n", None),
            flow.get("sourcePort", None),
            flow.get("destinationPort", None),
            flow.get("protocolName_n", None),
            flow.get("appName_n", None),
            flow.get("sourcePayloadAsUTF_n", None),
            flow.get("destinationPayloadAsUTF_n", None))

