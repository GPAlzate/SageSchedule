#
# The main driver of the academic planner app
#
from src.scraper import get_courses
import os

from flask import Flask, redirect
from flask import render_template
from flask import request
app = Flask(__name__)

df = get_courses()

# The home page
@app.route('/')
def index():
    return render_template('index.html', courses=None)

@app.route('/search')
def search():
    q = request.args.get('q')
    courses = None
    if q:
        courses = df[
            df['Course Number'].str.startswith(q.upper()) |
            df['Course Title'].str.contains(q, case=False)
        ]
    return render_template('index.html', courses=courses)

if __name__== '__main__':
    app.run(debug=True)
