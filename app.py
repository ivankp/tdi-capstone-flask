#!/usr/bin/env python3
import json
from flask import Flask, render_template, request, Response
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

with open('trends.json') as f:
    trends = json.load(f)

@app.route('/')
def index():
    with open('mech_cats.js') as f:
        mech_cats = f.read()
    return render_template('index.html',script=mech_cats)

@app.route('/eval',methods=['POST'])
def form_eval():
    req = json.loads(request.data)
    resp = { a: [ trends[a][v] ] for a,v in req.items() if v!='' }
    resp = json.dumps(resp,separators=(',',':'))
    return Response(resp,mimetype='application/json')

