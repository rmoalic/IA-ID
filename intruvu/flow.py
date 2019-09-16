from collections import Counter
from itertools import groupby
from functools import lru_cache
from statistics import mean
from operator import itemgetter

class Flow:

    def __init__(self, flow):
        """
        Constructor

        :param flow: a list of dict containing flows
        """
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
        """
        Get an histogram of flows by flow size

        :return: a "dict" with packet size as key and the number of occurrences as values
        """
        flow_size = [int(f["totalDestinationPackets"]) + int(f["totalSourcePackets"])
                     for f in self.flow
                     if "totalSourcePackets" in f and "totalDestinationPackets" in f]
        return Counter(flow_size)

    @lru_cache(maxsize=5)
    def __aggregate_in_out(self, name_in, name_out, key):
        """
        Calculate the average for name_in + name_out fields when grouping them by a key
        rough equivalent to "select key, avg(name_in + name_out) from flows group by key"

        :param name_in: the name of the first field
        :param name_out: the name of the second field
        :param key: the group by key
        :return: a dict with key as key and the average of the two fields as value
        """
        t = [(f[key], int(f[name_in]) + int(f[name_out]))
             for f in self.flow
             if name_in in f and name_out in f and key in f]
        t.sort(key=itemgetter(0))
        u = {key: mean([x[1] for x in group])
             for key, group in groupby(t, key=itemgetter(0))}
        return u

    @lru_cache(maxsize=5)
    def __aggregate_in_out_len(self, name_in, name_out, key):
        """
        Calculate the sum for both name_in and name_out fields when grouping them by a key
        rough equivalent to "select key, sum(name_in), sum(name_out) from flows group by key"

        :param name_in: the name of the first field
        :param name_out: the name of the second field
        :param key: the group by key
        :return: a dict with key as key and the sum of the two fields as value
        """
        # create tuple list [(key, size_a, size_b)] -> [("a", 3, 4), ("b", 2, 2), ("a", 1, 2)]
        t = [(f[key], len(f[name_in]), len(f[name_out]))
             for f in self.flow
             if name_in in f and name_out in f and key in f and f[name_in] is not None and f[name_out] is not None]
        # sort the tuple list by key -> [("a", 3, 4), ("a", 1, 2), ("b", 2, 2)]
        t.sort(key=itemgetter(0))
        # create a dictionary with key as key and sums last two members of the tuple -> | "a" -> [4, 6] "b" -> [2, 2] |
        u = {key: [sum(e)
                   for e in zip(*[(x[1],x[2])
                                  for x in group])]
             for key, group in groupby(t, key=itemgetter(0))}
        return u

    def __get_flows(self, name, value):
        """
        Return all the flows with flow[name] == value

        :param name: the name of the field to check
        :param value: the value to look for in the field
        :return: a list of flows
        """
        t = [flow for flow in self.flow if flow.get(name, None) == value]
        return t

    @lru_cache(maxsize=5)
    def __count(self, name):
        """
        Count the number of distinct values in a specified field of flows

        :param name: what field to count values from
        :return: a "dict" with different values as key and the number of occurrences as values
        """
        t = [flow.get(name, None) for flow in self.flow]
        return Counter(t)
