#!/usr/bin/env python3

import json, math
from collections import defaultdict

with open('../project/bgg_data_clean.json') as f:
    games = json.load(f)

cols  = games['columns']
index = games['index']
data  = games['data']

for i,x in enumerate(cols):
    globals()['i_'+x] = i

cols = [[i_mechanics,'m'],[i_categories,'c']]

trends = defaultdict(lambda: [ [0,0,0] for _ in range(22) ])

for g in data:
    y = g[i_year] - 2000
    r = g[i_rating]
    for i,a in cols:
        for x in g[i]:
            m = trends[f'{x} ({a})'][y]
            m[0] += 1
            m[1] += r
            m[2] += r*r

for y in trends.values():
    for m in y:
        if m[0] > 0:
            m[1] /= m[0]
            m[2] = math.sqrt(m[2]/m[0] - m[1]*m[1])

with open('trends.json','w') as f:
    json.dump(trends,f,separators=(',',':'))