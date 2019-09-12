import shelve
import matplotlib.pyplot as plt
from intruvu.flow import Flow
from intruvu.loader import load_files

FT = "fourre-tout"

with shelve.open(FT, 'c') as ft:
    load_files('./ISCX_train', ft)

ft = shelve.open(FT, 'r')

flow = Flow(ft[list(ft.keys())[1]])

per = flow.get_flows_per_packet()
plt.loglog(*zip(*sorted(per.items())), linestyle='None', marker=".")
plt.xlabel("packet/flow")
plt.ylabel("flows")
plt.show()

print(flow.get_protocols_count())
print(flow.get_protocols())
print(flow.get_flows_for_protocol("igmp"))
print(flow.get_applications_count())
print(flow.get_applications())
print(flow.get_flows_for_applications("WebMediaAudio"))
print(flow.get_protocols_bytes("tcp_ip"))
print(flow.get_protocols_packets("tcp_ip"))
ft.close()
