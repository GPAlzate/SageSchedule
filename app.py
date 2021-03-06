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
    # session.clear()
    if 'school_year' not in session:
        session['school_year'] = SCHOOL_YEAR
    if 'semesters' not in session:
        session['num_sems'] = NUM_SEMS
        create_semesters()
    if 'breadth_reqs' not in session:
        session['breadth_reqs'] = [None] * 6
    if 'overlay_reqs' not in session:
        session['overlay_reqs'] = {
            'Analyzing Difference' : None,
            'Writing Intensive' : None,
            'Speaking Intensive' : None
        }
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

    # add course to session
    session[sem].append(course)

    # update fulfilled breadth reqs
    area = course['Breadth Area']
    num = int(course['Breadth Area'][-1]) if area else None
    if num and not session['breadth_reqs'][num-1]:
        session['breadth_reqs'][num -1] = course

    # update overlays (a course can only fulfill one overlay)
    overlay_reqs = session['overlay_reqs']
    if not overlay_reqs['Analyzing Difference'] and course['Analyzing Difference']:
        overlay_reqs['Analyzing Difference'] = course
    elif not overlay_reqs['Writing Intensive'] and course['Writing Intensive']:
        overlay_reqs['Writing Intensive'] = course
    elif not overlay_reqs['Speaking Intensive'] and course['Speaking Intensive']:
        overlay_reqs['Speaking Intensive'] = course

    session.modified = True
    return course

if __name__== '__main__':
    app.run(debug=True)
