#
# The main driver of the academic planner app
#
from src.scraper import get_courses
import os

from flask import Flask
from flask import render_template
app = Flask(__name__)

# The home page
@app.route('/')
def index():
    prefix = 'MATH'
    courses = df[df['Course Number'].str.startswith(prefix)]
    return render_template('index.html', courses=courses.to_html(index=False))

if __name__== '__main__':
    df = get_courses()
    app.run(debug=True)