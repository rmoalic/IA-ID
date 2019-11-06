from murmurhash import hash
import re

def direction_converter(direction):
    ret = (0, 0)
    if direction == "L2R":
        ret = (0, 1)
    elif direction == "R2L":
        ret = (1, 0)
    elif direction == "L2L":
        ret = (0, 0)
    elif direction == "R2R":
        ret = (1, 1)
    return ret

def protocol_converter(protocol):
    protocols = ['tcp_ip', 'udp_ip', 'icmp_ip', 'igmp', 'ip', 'ipv6icmp', 'unknown']
    pos = [1 if protocol == k else 0 for k in protocols]
    if sum(pos) != 1:
        pos[-1] = 1
    return tuple(pos)


def payload_hist(data):
    array = {chr(x): 0 for x in range(255)}
    if data is None:
        return array.values()
    ascii_data = list(re.sub("[^\x00-\xff]", "", data))
    for d in ascii_data:
        array[d] = array[d] + 1
    assert len(array) == 255
    return array.values()


def insert_numerical_values(flow):
    if ("protocolName" not in flow):
        print("warning: no protocol name, vectorisation impacted for flow")
        return
    flow["protocolName_n"] = protocol_converter(flow.get("protocolName", None))
    flow["source_n"] = tuple([int(e) for e in flow["source"].split('.')])
    flow["destination_n"] = tuple([int(e) for e in flow["destination"].split('.')])
    flow["direction_n"] = direction_converter(flow["direction"])
    flow["sourcePayloadAsUTF_n"] = tuple(payload_hist(flow.get("sourcePayloadAsUTF", None)))
    flow["destinationPayloadAsUTF_n"] = tuple(payload_hist(flow.get("destinationPayloadAsUTF", None)))

def make_vector(flow):
    return (flow.get("totalSourceBytes", 0),
            flow.get("totalDestinationBytes", 0),
            flow.get("totalSourcePackets", 0),
            flow.get("totalDestinationPackets", 0),
            *flow.get("source_n", (0,0,0,0)),
            *flow.get("destination_n", (0,0,0,0)),
            *flow.get("direction_n", (0,0)),
            flow.get("sourcePort", 0),
            flow.get("destinationPort", 0),
            *flow.get("protocolName_n", tuple([0 for x in range(7)])),
            *flow.get("sourcePayloadAsUTF_n", tuple([0 for x in range(255)])),
            *flow.get("destinationPayloadAsUTF_n", tuple([0 for x in range(255)])))

