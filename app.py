from flask import Flask, render_template
from jobs.yaml_parser import YamlParser

app = Flask(__name__)


@app.route('/')
def hello():
    yp = YamlParser()
    return render_template('index.html', terms=yp.terms)
