

class Flow:

    def __init__(this, flow):
        this.flow = flow


    def get_protocols(this):
        t = [flow.get("protocolName", None) for flow in this.flow]
        return set(t)

    def get_flows_for_protocol(this, protocol):
        t = [flow for flow in this.flow if flow.get("protocolName", None) == protocol]
        return t

