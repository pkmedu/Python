#Ex4_chart.py
# Obtained from the web - source yet to be cited
from graphviz import Digraph
A=[('HW', 'Root'), ('SW', 'Root'),
  ('Electric', 'HW'), ('ink', 'HW'), ('windows', 'SW'), ('Drivers', 'SW'),
  ('Yellow', 'ink'), ('blue', 'ink'), ('pink', 'ink'),
  ('FE', 'Drivers'), ('BE', 'Drivers')]
e = Digraph()
e.attr(rankdir='LR')
for a in A:
    e.node(a[0])
    e.edge(a[0], a[1])
e.view()
