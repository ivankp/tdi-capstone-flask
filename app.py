#!/usr/bin/env python3

import json

from flask import Flask, render_template, request, Response
from flask_compress import Compress

from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import json_item
from bokeh.resources import CDN
from bokeh.models import Range1d, HoverTool

import numpy as np

import dill, lzma
# import time

app = Flask(__name__)
Compress(app)

with open('attrs.js') as f:
    attrs = f.read()

with open('trends.json') as f:
    trends = json.load(f)

with lzma.open('model.dill.xz') as f:
    # t = time.process_time()
    globals().update(dill.load(f))
    # elapsed_time = time.process_time() - t
    # print(f'model data loaded in {elapsed_time:.2} sec')

@app.route('/')
def index():
    return render_template('index.html',
        script=attrs, head=CDN.render()
    )

@app.route('/eval',methods=['POST'])
def form_eval():
    req = json.loads(request.data)

    # get ML model prediction ---------------------------------------
    attrs_encoded = np.zeros(len(attr_map),dtype=int)
    for attr in req['attrs']:
        i = attr_map.get(attr,None)
        if not (i is None):
            attrs_encoded[i] = 1
    # print(attrs_encoded)

    attrs_pca = pca.transform(attrs_encoded.reshape(1,-1))
    # print(attrs_pca)
    # print(attrs_pca[0,:2])

    rating = forest.predict(attrs_pca)
    # print(rating)

    # plots trends for selected attributes --------------------------
    trend_plots = [ ]
    for attr in req['attrs']:
        trend = trends.get(attr,None)
        if trend is None: continue

        test = list(range(22))

        fig = figure(
            width = 800, height = 400,
            title = attr,
            x_axis_label = 'Year',
            y_axis_label = 'Average Rating',
            tools = [
                'save',
                HoverTool(
                    names=['this_o','other_o'],
                    tooltips = [
                        ('year','@year'),
                        ('num','@num'),
                        ('rating','@rating{0.00}'),
                        ('stdev','@stdev{0.00}')
                    ]
                )
            ]
        )
        fig.x_range = Range1d(2000-0.5,2021+0.5)

        for t,(name,color) in zip(trend, (
            ('this','#FF7F0E'),
            ('other','#1F77B4')
        )):
            source = ColumnDataSource( dict(zip(
                ['year','num','rating','stdev'],
                zip(*(
                    [ i+2000, *x ]
                    for i,x in enumerate(t)
                    if x[0] > 0
                ))
            )))

            fig.line(
                'year', 'rating',
                source = source,
                name = f'{name}_o',
                line_width = 2,
                color = color,
                legend_label = name
            )
            fig.circle(
                'year', 'rating',
                source = source,
                size = 6,
                color = color,
                legend_label = name,
            )

        fig.legend.location = 'top_left'

        trend_plots.append(json_item(fig,attr))

    return Response(
        json.dumps({
            'trends': trend_plots,
            'ml': {
                'pca': attrs_pca[0,:2].tolist(),
                'rating': rating[0]
            }
        },separators=(',',':')),
        mimetype='application/json')

if __name__ == '__main__':
    app.run()
