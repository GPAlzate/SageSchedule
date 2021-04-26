#
# The main driver of the academic planner app
#
from src.scraper import get_courses

import os
import re

from flask import Flask, redirect, render_template, request, session
app = Flask(__name__)
app.secret_key = 'all our celebrities keep dying'

df = get_courses()

# The home page
@app.route('/')
def index():
    if 'school_year' not in session:
        session['school_year'] = 21
    if 'semesters' not in session:
        session['semesters'] = 8
    print(session['semesters'])
    return render_template('index.html', courses=None)

@app.route('/search')
def search():
    q = request.args.get('q')
    courses = None
    if q:

        # split query by non-alphanum characters
        keywords = re.split('[^a-zA-Z0-9]', q)

        # regex query: contains all of the keywords
        pattern = ''.join([f"(?=.*{w})" for w in keywords]) + ".+"
        courses = df[
            df['Course Title'].str.contains(pattern, regex=True, case=False) |
            df['Course Number'].str.contains(pattern, regex=True, case=False)
        ]
        
    return render_template('index.html', courses=courses)

if __name__== '__main__':
    app.run(debug=True)
