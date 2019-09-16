from collections import Counter
from itertools import groupby
from functools import lru_cache
from operator import itemgetter

#TODO: get the source and destination Payload size for each protocol
#     get the source and destination Payload size for each application


class Flow:

    def __init__(self, flow):
        self.flow = flow

    def get_protocols(self):
        """Get the list of all the (distinct) protocols contained in the XML files"""
        protocols_count = self.__count("protocolName")
        return list(protocols_count.keys())

    def get_flows_for_protocol(self, protocol):
        """Get the list of flows for a given protocol"""
        return self.__get_flows("protocolName", protocol)

    def get_flows_count_by_protocol(self):
        """Get the number of flows for each protocols"""
        protocols_count = self.__count("protocolName")
        return dict(protocols_count)

    def get_payload_by_protocol(self):
        """Get the source and destination Payload size for each protocol"""
        protocols_payloads = self.__aggregate_in_out_len("sourcePayloadAsUTF", "destinationPayloadAsUTF", "protocolName")
        return dict(protocols_payloads)

    def get_bytes_count_by_protocol(self):
        """Get the total source/destination Bytes for each protocol"""
        protocols_bytes = self.__aggregate_in_out("totalSourceBytes", "totalDestinationBytes", "protocolName")
        return dict(protocols_bytes)

    def get_packets_count_by_protocol(self):
        """Get the total source/destination packets for each protocol"""
        protocols_packets = self.__aggregate_in_out("totalSourcePackets", "totalDestinationPackets", "protocolName")
        return dict(protocols_packets)

    def get_applications(self):
        """Get the list of all the (distinct) applications contained in the XML files"""
        applications_count = self.__count("appName")
        return list(applications_count.keys())

    def get_flows_for_application(self, app):
        """Get the list of flows for a given application"""
        return self.__get_flows("appName", app)

    def get_flows_count_by_application(self):
        """Get the number of flows for each application"""
        applications_count = self.__count("appName")
        return dict(applications_count)

    def get_payload_by_application(self):
        """Get the source and destination Payload size for each application"""
        applications_payloads = self.__aggregate_in_out_len("sourcePayloadAsUTF", "destinationPayloadAsUTF", "appName")
        return dict(applications_payloads)

    def get_bytes_count_by_application(self):
        """Get the total source/destination Bytes for each application"""
        applications_bytes = self.__aggregate_in_out("totalSourceBytes", "totalDestinationBytes", "appName")
        return dict(applications_bytes)

    def get_packets_count_by_application(self):
        """Get the total source/destination packets for each application"""
        applications_packets = self.__aggregate_in_out("totalSourcePackets", "totalDestinationPackets", "appName")
        return dict(applications_packets)

    def get_flows_per_packet(self):
        flow_size = [int(f["totalDestinationPackets"]) + int(f["totalSourcePackets"]) for f in self.flow if "totalSourcePackets" in f and "totalDestinationPackets" in f]
        return Counter(flow_size)

    @lru_cache(maxsize=5)
    def __aggregate_in_out(self, name_in, name_out, key):
        t = [(f[key], int(f[name_in]) + int(f[name_out])) for f in self.flow
             if name_in in f and name_out in f and key in f]
        t.sort(key=itemgetter(0))
        u = {key: sum(x[1] for x in group) for key, group in groupby(t, key=itemgetter(0))}
        return u

    @lru_cache(maxsize=5)
    def __aggregate_in_out_len(self, name_in, name_out, key):
        t = [(f[key], len(f[name_in]), len(f[name_out])) for f in self.flow
             if name_in in f and name_out in f and key in f and f[name_in] is not None and f[name_out] is not None]
        t.sort(key=itemgetter(0))
        u = {key: (sum(x[1] for x in group), sum(x[2] for x in group)) for key, group in groupby(t, key=itemgetter(0))}
        return u

    def __get_flows(self, name, value):
        t = [flow for flow in self.flow
             if flow.get(name, None) == value]
        return t

    @lru_cache(maxsize=5)
    def __count(self, name):
        t = [flow.get(name, None) for flow in self.flow]
        return Counter(t)
