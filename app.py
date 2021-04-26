#
# The main driver of the academic planner app
#
from src.scraper import get_courses
from fuzzywuzzy import fuzz

import os

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
    threshold = 45
    if q:

        # courses = df[
        #     df.apply(lambda row: fuzz.token_sort_ratio(row['Course Title'], q), axis=1) > threshold
        # ]
        
        # courses2 = courses[
        #     courses['Course Number'].str.startswith(q.upper()) |
        #     courses['Course Title'].str.contains(q, case=False)
        # ]
     
        courses = df[
            df.apply(lambda row: fuzz.token_sort_ratio(row['Course Title'], q), axis=1) > threshold 
             # fuzz.token_sort_ratio(q, df['Course Number'].str) > threshold |
             # fuzz.token_sort_ratio(q, df['Course Title'].str) > threshold |
             # df['Course Number'].str.startswith(q.upper()) |
             # df['Course Title'].str.contains(q, case=False)
         ]
        
        # courses = df[df.apply(lambda row: fuzz.token_sort_ratio(row['Course Title'], q), axis=1) > threshold]

    return render_template('index.html', courses=courses)

def get_ratio(q, row):
    name = row['Course Title']
    return fuzz.token_sort_ratio(name, q)


if __name__== '__main__':
    app.run(debug=True)
