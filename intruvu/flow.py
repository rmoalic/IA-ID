
class Flow:

    def __init__(self, flow):
        self.flow = flow

    def get_protocols(self):
        t = [flow.get("protocolName", None) for flow in self.flow]
        return set(t)

    def get_flows_for_protocol(self, protocol):
        t = [flow for flow in self.flow
             if flow.get("protocolName", None) == protocol]
        return t
