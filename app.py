#
# The main driver of the academic planner app
#
import scraper

from flask import Flask
from flask import render_template
app = Flask(__name__)

# The home page
@app.route('/')
def index():
    return render_template('index.html', majors=scraper.MAJOR_DICT)

if __name__== '__main__':
    app.run(debug=True)