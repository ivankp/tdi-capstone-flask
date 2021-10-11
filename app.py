#!/usr/bin/env python3

import json

from flask import Flask, render_template, request, Response
from flask_compress import Compress

from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.resources import CDN

app = Flask(__name__)
Compress(app)

with open('attrs.js') as f:
    attrs = f.read()

with open('trends.json') as f:
    trends = json.load(f)

@app.route('/')
def index():
    return render_template('index.html',
        script=attrs, head=CDN.render())

@app.route('/eval',methods=['POST'])
def form_eval():
    req = json.loads(request.data)

    selected_trends = [ ]
    for attr in req['attrs']:
        trend = trends.get(attr,None)
        if trend is None: continue

        fig = figure(
            width=800, height=400,
            tools='save',
            title = attr,
            x_axis_label='Year',
            y_axis_label='Average Rating',
        )

        xs = [ x+2000 for x in range(len(trend)) ]
        ys = [ x[1] for x in trend ]
        fig.line(
            xs, ys,
            legend_label = 'this',
            line_width = 2
        )
        fig.circle(
            xs, ys,
            size = 5
        )

        fig.legend.location = 'top_left'

        selected_trends.append(json_item(fig,attr))

    return Response(
        json.dumps({
            'trends': selected_trends
        },separators=(',',':')),
        mimetype='application/json')

