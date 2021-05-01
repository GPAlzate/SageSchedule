#
# The main driver of the academic planner app
#
from src.scraper import get_courses

import os
import re
import json

from flask import Flask, redirect, render_template, request, session, jsonify

SCHOOL_YEAR = 21
NUM_SEMS = 8

app = Flask(__name__)
app.secret_key = 'all our celebrities keep dying'

df = get_courses()

def create_semesters():
    semesters = []
    for i in range(NUM_SEMS):
        # create a dictionary of semesters in session
        # each sem will store the courses selected by the user
        sem = f"{'Spring' if i % 2 else 'Fall'} '{SCHOOL_YEAR + (i + 1)//2}"
        semesters.append(sem)
        session[sem] = []

    # save the dictionary of semester strings
    session['semesters'] = semesters

# The home page
@app.route('/')
def index():
    session.clear()
    if 'school_year' not in session:
        print('Setting school year to ', SCHOOL_YEAR)
        session['school_year'] = SCHOOL_YEAR
    if 'semesters' not in session:
        print('Setting number of semesters to ', NUM_SEMS)
        session['num_sems'] = NUM_SEMS
        create_semesters()
    for n in session:
        print(f'{n}:{session[n]}')
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

@app.route('/addCourse', methods=['POST'])
def addCourse():
    data = request.get_json()
    sem = data['sem']
    course = json.loads(data['course'])
    session[sem].append(course)
    session.modified = True
    return data

if __name__== '__main__':
    app.run(debug=True)
