from collections import Counter
from itertools import groupby
from functools import lru_cache

#TODO get the source and destination Payload size for each protocol
#     get the source and destination Payload size for each application


class Flow:

    def __init__(self, flow):
        self.flow = flow

    def get_protocols(self):
        protocols_count = self.__count("protocolName")
        return list(protocols_count.keys())

    def get_protocols_count(self):
        protocols_count = self.__count("protocolName")
        return dict(protocols_count)

    def get_protocols_packets(self, protocol):
        protocols_packets = self.__aggregate_in_out("totalSourcePackets","totalDestinationPackets","protocolName")
        return protocols_packets.get(protocol, None)

    def get_protocols_bytes(self, protocol):
        protocols_bytes = self.__aggregate_in_out("totalSourceBytes","totalDestinationBytes","protocolName")
        return protocols_bytes.get(protocol, None)

    def get_flows_for_protocol(self, protocol):
        return self.__get_flows("protocolName", protocol)

    def get_applications(self):
        applications_count = self.__count("appName")
        return list(applications_count.keys())

    def get_applications_count(self):
        applications_count = self.__count("appName")
        return dict(applications_count)

    def get_flows_for_applications(self, app):
        return self.__get_flows("appName", app)

    @lru_cache(maxsize=5)
    def __aggregate_in_out(self, name_in, name_out, key):
        t = [(f[key], int(f[name_in]) + int(f[name_out])) for f in self.flow
             if name_in in f and name_out in f]
        u = t.sort(key=lambda x: x[0])
        u = {key: sum(x[1] for x in group) for key, group in groupby(t, key=lambda x: x[0])}
        return u

    def __get_flows(self, name, value):
        t = [flow for flow in self.flow
             if flow.get(name, None) == value]
        return t

    @lru_cache(maxsize=5)
    def __count(self, name):
        t = [flow.get(name, None) for flow in self.flow]
        return Counter(t)