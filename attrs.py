#!/usr/bin/env python3

import json
from collections import defaultdict

with open('../project/bgg_data_clean.json') as f:
    games = json.load(f)

cols  = games['columns']
index = games['index']
data  = games['data']

for i,x in enumerate(cols):
    globals()['i_'+x] = i

mechs = set()
cats  = set()

for g in data:
    mechs.update(g[i_mechanics])
    cats .update(g[i_categories])

attrs = [
    [ f'{x} ({t})' for x in a ]
    for a,t in [[mechs,'m'],[cats,'c']]
]
attrs = json.dumps( sorted( attrs[0]+attrs[1] ), separators=(',',':') )

with open('attrs.js','w') as f:
    f.write(f'const all_attributes = {attrs};\n')
