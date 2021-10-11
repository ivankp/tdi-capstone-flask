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

with open('mech_cats.js','w') as f:
    f.write(f'const all_mechanics = {sorted(mechs)};\n')
    f.write(f'const all_categories = {sorted(cats)};\n')
