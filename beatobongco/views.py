from flask import Blueprint, render_template, redirect, url_for, abort, request, Response
from functools import wraps
from app import app 
from models import Post 
from time import strftime, localtime
import os, datetime
import mistune

# from time import strftime, localtime
# from collections import OrderedDict
# from operator import itemgetter

# Custom filter for jinja
@app.template_filter()
def get_date(value):
  return strftime('%B %e, %Y', localtime(value))

@app.template_filter()
def split_comma(value):
  return [x.strip() for x in value.split(',')]

@app.template_filter()
def get_preview(value):
  return '\n'.join(value.split('\n')[1:4])

@app.template_filter()
def mistunify(value):
  return mistune.markdown(value)

app.jinja_env.filters['get_date'] = get_date
app.jinja_env.filters['split_comma'] = split_comma
app.jinja_env.filters['get_preview'] = get_preview
app.jinja_env.filters['mistunify'] = mistunify

### SECTION: Basic auth ###

def check_auth_notebook(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['N_USER'] and password == app.config["N_PASS"]

def check_auth_blog(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['B_USER'] and password == app.config["B_PASS"]

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def notebook_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth_notebook(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def blog_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_auth_blog(auth.username, auth.password):
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
                'created' : os.path.getctime( directory + file ), 
                'title' : myarticle.readline().replace('#',''),
                'preview' : ''.join(myarticle.readlines()[1:4]),
                # Get the last level of the directory
                'url' : category + '/' + file.replace('.md',''),
                'category' : category
                })
                
          except IOError:
            pass
  
  all_articles.sort(key=lambda x: x['created'], reverse=True)

  return all_articles

def get_contents(article, path):
  """ Gets the contents of an .md file from a path as a string.

  article -- .md filename without the extension 
  path -- directory where .md file is located

  """
  # article_url = url_for('static', filename=path.split('/')[-1] + article + '.md') 
  file_content = {}
  try:
    with open(path + article + ".md", 'r') as myarticle:
      content = myarticle.read()
      file_content = { 'full_text': content, 'body' : '\n'.join(content.split('\n')[1:]), 'title' : content.split('\n', 1)[0], 'date' : os.path.getctime( path + article + ".md") }
  except IOError:
    abort(404)
  return file_content

### END SECTION ###

@app.route("/")
def index():
  return redirect(url_for('blog'))

@app.route("/blog/")
@app.route("/blog")
def blog():
  # get all titles of blog entries
  posts = Post.query.all()

  return render_template('index.html', articles=posts, title="beatobongco.com", heading="Stuff I've Written", category="blog", is_notes=False)

@app.route("/blog/<article>/")
@app.route("/blog/<article>")
def show_blog(article):
  contents = Post.query.filter_by(url=article).first()

  return render_template('blog.html', 
    article=contents,
    title=contents.title + " - beatobongco.com"
  )

@app.route("/blog/<article>/edit")
@blog_auth
def edit_blog(article):
  if request.method == 'POST':
    url = request.form['url']
    title = request.form['title']
    preview = request.form['preview']
    image = request.form['preview_image']
    category = request.form['category']
    body = request.form['body']
    
    test = Post(url, title, preview, category, body, image)

    db.session.add(test)
    db.session.commit()

  contents = Post.query.filter_by(url=article).first()

  return render_template('blogeditor.html', 
    url=contents.url,
    title=contents.title, 
    preview=contents.preview,
    preview_image=contents.image,
    category=contents.category,
    body=contents.body
  )

@app.route("/notes/")
@app.route("/notes")
def notes():
  articles = pyrachnid([notes_directory])
  return render_template('index.html', articles=articles, title="Notes", heading="My Autosaving Markdown Notebook in the Sky", is_notes=True)

@app.route("/notes/<article>/")
@app.route("/notes/<article>")
def show_note(article):
  contents = get_contents(article, notes_directory)
  return render_template('notes.html', title=contents.get('title'), content=contents.get('body'), date=contents.get('date'), editable=True)

@app.route("/notes/<article>/edit", methods=['GET', 'POST'])
@notebook_auth
def edit_note(article):
  if request.method == 'POST':
    updated = request.form['article']

    app.logger.debug(updated)

    with open(notes_directory + '/' + article + '.md', 'w') as f:
      f.write(updated)

  contents = get_contents(article, notes_directory)
  return render_template('noteeditor.html', title=contents.get('title'), content=contents.get('full_text'))

@app.route("/about/")
@app.route("/about")
def about_me():
  return render_template('about.html', title="About Me - beatobongco.com")


@app.route("/projects/")
@app.route("/projects")
def projects():
  return render_template('projects.html', title="Projects - beatobongco.com", heading="Projects")