from flask import Blueprint, render_template, redirect, url_for, abort, request, Response
from functools import wraps
from app import app 

import os

from time import strftime, localtime
from collections import OrderedDict
from operator import itemgetter

# Custom filter for jinja
@app.template_filter()
def get_date(value):
    return strftime('%d %B %Y %I:%M %p', localtime(value))

app.jinja_env.filters['get_date'] = get_date

### SECTION: Basic auth ###

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['USERNAME'] and password == app.config["PASSWORD"]

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

### END SECTION ###

### SECTION: Global Variables ###
preview_lines = 4;

root_directory = os.path.dirname(os.path.abspath(__file__));
static_directory = root_directory  + "/static/"

blog_directory = static_directory + "blog/"
notes_directory = static_directory + "notes/"

### END SECTION ###

### SECTION: Functions ###

def pyrachnid(article_directories):
  """Returns a list containing data about .md files contained in a directory.

  article_directories -- a list of directories (absolute path)
  """ 
  all_articles = []

  if(type(article_directories) == list):
    for directory in article_directories:
      for file in os.listdir(directory):
        if file.endswith(".md"):
          try:
            with open(directory+file, 'r') as myarticle:
              category = directory.split('/')[-2]
              all_articles.append({ 
                'date' : os.path.getctime( directory + file ), 
                'name' : myarticle.readline().replace('#',''),
                'preview' : ''.join(myarticle.readlines()[1:preview_lines]),
                # Get the last level of the directory
                'url' : request.url_root + category + '/' + file.replace('.md',''),
                'category' : category
                })
                
          except IOError:
            pass
  
  all_articles.sort(key=lambda x: x['date'], reverse=True)

  return all_articles

def get_contents(article, path):
  """ Gets the contents of an .md file from a path as a string.

  article -- .md filename without the extension 
  path -- directory where .md file is located

  """
  article_url = url_for('static', filename=path.split('/')[-1] + article + '.md') 

  try:
    with open(path + article + ".md", 'r') as myarticle:
      file_content = myarticle.read()
  except IOError:
    abort(404)
  return file_content

### END SECTION ###

@app.route("/")
def index():
  # get all titles of blog entries
  articles = pyrachnid([blog_directory, notes_directory])
  return render_template('index.html', articles=articles, title="beatobongco.com", heading="Recent Activity")

@app.route("/blog")
def blog():
  articles = pyrachnid([blog_directory])
  return render_template('index.html', articles=articles, title="Blog", heading="Stuff I've Written")

@app.route("/blog/<article>")

def show_blog(article):
  contents = get_contents(article, blog_directory)

  return render_template('pages.html', title=contents.split('\n', 1)[0].replace("#",""), content=contents)

@app.route("/notes")
def notes():
  articles = pyrachnid([notes_directory])
  return render_template('index.html', articles=articles, title="Notes", heading="My Notebook in the Sky")

@app.route("/notes/<article>")
def show_note(article):
  contents = get_contents(article, notes_directory)
  return render_template('pages.html', title=contents.split('\n', 1)[0].replace("#",""), content=contents, editable=True)

@app.route("/notes/<article>/edit", methods=['GET', 'POST'])
@requires_auth
def edit_note(article):
  if request.method == 'POST':
    updated = request.form['article']

    app.logger.debug(updated)

    with open(notes_directory + '/' + article + '.md', 'w') as f:
      f.write(updated)

  contents = get_contents(article, notes_directory)
  return render_template('editor.html', title=contents.split('\n', 1)[0].replace("#",""), content=contents)