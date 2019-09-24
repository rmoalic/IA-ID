import pyhash

hash = pyhash.murmur1_32()

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


def insert_numerical_values(flow):
    flow["appName_n"] = hash(flow["appName"])
    flow["protocolName_n"] = hash(flow["protocolName"])
    flow["source_n"] = int(''.join(flow["source"].split('.')))
    flow["destination_n"] = int(''.join(flow["destination"].split('.')))
    flow["direction_n"] = direction_converter(flow["direction"])

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
            flow.get("appName_n", None))

