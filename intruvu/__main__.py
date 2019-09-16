import shelve
import matplotlib.pyplot as plt
from intruvu.flow import Flow
from intruvu.loader import load_files

FT = "fourre-tout"

with shelve.open(FT, 'c') as ft:
    load_files('./ISCX_train', ft)

ft = shelve.open(FT, 'r')

# flow = Flow(ft[list(ft.keys())[1]])
flow = Flow([x for xs in ft.values() for x in xs])

per = flow.get_flows_per_packet()
plt.loglog(*zip(*sorted(per.items())), linestyle='None', marker=".")
plt.xlabel("packet/flow")
plt.ylabel("flows")
plt.show()

print(flow.get_protocols())
print(flow.get_flows_for_protocol("igmp"))
print(flow.get_flows_count_by_protocol())
print(flow.get_payload_by_protocol())
print(flow.get_bytes_count_by_protocol())
print(flow.get_packets_count_by_protocol())
print(flow.get_applications())
print(flow.get_flows_for_application("WebMediaAudio"))
print(flow.get_payload_by_application())
print(flow.get_bytes_count_by_application())
print(flow.get_packets_count_by_application())

ft.close()
