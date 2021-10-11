#!/usr/bin/env python3
import json
from flask import Flask, render_template, request, Response
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

with open('attrs.js') as f:
    attrs = f.read()

with open('trends.json') as f:
    trends = json.load(f)

@app.route('/')
def index():
    return render_template('index.html',script=attrs)

@app.route('/eval',methods=['POST'])
def form_eval():
    req = json.loads(request.data)
    resp = {
        'trends': { x: trends[x] for x in req['attrs'] if x in trends }
    }
    resp = json.dumps(resp,separators=(',',':'))
    return Response(resp,mimetype='application/json')

