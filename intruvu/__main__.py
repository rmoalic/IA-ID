import shelve
from intruvu.Flow import Flow
from intruvu.loader import load_files

FT = "fourre-tout"

with shelve.open(FT, 'c') as ft:
    load_files('./ISCX_train', ft)

ft = shelve.open(FT, 'r')

flow = Flow(ft[list(ft.keys())[0]])
print(flow.get_protocols())

ft.close()
