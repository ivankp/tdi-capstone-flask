#!/usr/bin/env python3

import json

from flask import Flask, render_template, request, Response
from flask_compress import Compress

from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import json_item
from bokeh.resources import CDN
from bokeh.models import Range1d, HoverTool

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

        selected_trends.append(json_item(fig,attr))

    return Response(
        json.dumps({
            'trends': selected_trends
        },separators=(',',':')),
        mimetype='application/json')

if __name__ == '__main__':
    app.run()
