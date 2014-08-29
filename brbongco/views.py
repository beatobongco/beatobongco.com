from flask import Blueprint, render_template, redirect, url_for, abort
from app import app 

import os
import time
from collections import OrderedDict
from operator import itemgetter

#Variables
static_directory = os.path.dirname(os.path.abspath(__file__)) + "/static/"
pages_path = "pages/"
pages_directory = static_directory + pages_path


# Functions

def get_contents(article):
  article_url = url_for('static', filename=pages_path + article + '.md') 
  try:
    with open(pages_directory + article + ".md", 'r') as myarticle:
      file_content = myarticle.read()
  except IOError:
    abort(404)
  return file_content

@app.route("/")

def index():
  # get all titles of blog entries
  all_articles = []

  for file in os.listdir(pages_directory):
    if file.endswith(".md"):
      try:
        with open(pages_directory+file, 'r') as myarticle:
          app.logger.debug("!")
          all_articles.append({ 'date' : time.strftime('%d %B %Y %I:%M %p', 
            time.localtime(os.path.getctime(pages_directory + file))), 
          'url' : pages_path + file.replace('.md',''), 
          'name' : myarticle.readline().replace('#',''),
          'preview' : ''.join(myarticle.readlines()[1:4]) })
          
      except IOError:
        pass

  app.logger.debug(all_articles)

  all_articles.sort(key=lambda x: x['date'], reverse=True)

  return render_template('index.html', articles=all_articles, title="brbongco.com")

@app.route("/pages/<article>")

def show_page(article):
  contents = get_contents(article)

  return render_template('pages.html', title=contents.split('\n', 1)[0].replace("#",""), content=contents)

@app.route("/pages/<article>/edit")

def edit_page(article):
  # need some sort of authentication for editing
  contents = get_contents(article)
  return render_template('editor.html', title=contents.split('\n', 1)[0].replace("#",""), content=contents)