from murmurhash import hash
import re


def direction_converter(direction):
    """
    Convert a direction string to a tuple
    if the parameter is incorrect returns (-1, -1)

    >>> direction_converter("L2R")
    (0, 1)
    >>> direction_converter("?")
    warning: incorrect direction string  ?
    (-1, -1)

    :param direction: direction string eg "L2R"
    :return: a tuple with 2 values between 0 and 1 (R, L)
    """
    ret = (-1, -1)
    if direction == "L2R":
        ret = (0, 1)
    elif direction == "R2L":
        ret = (1, 0)
    elif direction == "L2L":
        ret = (0, 0)
    elif direction == "R2R":
        ret = (1, 1)
    else:
        print('warning: incorrect direction string ', direction)
    return ret


def protocol_converter(protocol):
    """
    Convert a protocol string to a tuple

    >>> protocol_converter('ip')
    (0, 0, 0, 0, 1, 0, 0)
    >>> protocol_converter('?')
    (0, 0, 0, 0, 0, 0, 1)

    :param protocol: protocol name string
    :return: a tuple of size 7 with all values at 0 except one at 1
    """
    protocols = ['tcp_ip', 'udp_ip', 'icmp_ip', 'igmp', 'ip', 'ipv6icmp', 'unknown']
    pos = [1 if protocol == k else 0 for k in protocols]
    if sum(pos) != 1:
        pos[-1] = 1
    return tuple(pos)


def payload_hist(data):
    """
    Create an histogram of the ascii characters present in the input string
    Non ascii characters are ignored

    :param data: string of characters
    :return: dict with 255 entries (characters number -> number of occurrences in data)
    """
    array = {chr(x): 0 for x in range(255)}
    if data is None:
        return array.values()
    ascii_data = list(re.sub("[^\x00-\xff]", "", data))
    for d in ascii_data:
        array[d] = array[d] + 1
    assert len(array) == 255
    return array.values()


def insert_numerical_values(flow):
    """
    Insert vectorised version of some of the keys of a flow into itself
    new keys have a "_n" suffix

    :param flow: a flow
    """
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
    """
    Create a vector from a flow

    :param flow: a flow
    :return: a tuple of size 533
    """
    ret =  (flow.get("totalSourceBytes", 0),
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
    assert len(ret) == 533
    return ret

