import json

class FlowES:

    def __init__(self, es, index_name):
        self.es = es
        self.index_name = index_name

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
    pass

    def __count(self, name):
        agg = {
            "size": 0,
            "query": {
                "match_all": {}
            },
            "aggs": {
                "group_by": {
                    "terms":{
                     "field": name+".keyword"
                    }
                }
            }
        }
        try:
            hits = self.es.search(index=self.index_name, body=json.dumps(agg))
            H = hits['aggregations']
            A = H['group_by']['buckets']
        except Exception as e:
            print(e)
            A = dict()
        return {h['key']: h['doc_count'] for h in A}

    def __aggregate_in_out(self, name_in, name_out, key):
        """
        Calculate the average for name_in + name_out fields when grouping them by a key
        rough equivalent to "select key, avg(name_in + name_out) from flows group by key"

        :param name_in: the name of the first field
        :param name_out: the name of the second field
        :param key: the group by key
        :return: a dict with key as key and the average of the two fields as value
        """
        agg = {
            "size": 0,
            "query": {
                "match_all": {}
            },
            "aggs": {
                "group_by": {
                    "terms": {
                        "field": key+".keyword"
                    },
                    "aggs": {
                        "res": {
                            "avg": {
                                "script": {
                                    "lang": "expression",
                                    "source": "doc['{}'] + doc['{}']".format(name_in, name_out)
                                }
                            }
                        }
                    }
                }
            }
        }
        try:
            hits = self.es.search(index=self.index_name, body=json.dumps(agg))
            H = hits['aggregations']
            A = H['group_by']['buckets']
        except Exception as e:
            print(e)
            A = dict()
        return {h['key']: h['res']['value'] for h in A}
