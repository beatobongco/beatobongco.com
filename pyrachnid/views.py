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

@app.route("/")

def index():
  # get all titles of blog entries
  all_articles = []

  for file in os.listdir(pages_directory):
    if file.endswith(".md"):
      try:
        with open(pages_directory+file, 'r') as myarticle:
          app.logger.debug("!")
          all_articles.append({ 'date' : time.strftime('%d %B %Y %I:%M %p', time.gmtime(os.path.getctime(pages_directory + file))), 'url' : pages_path + file.replace('.md',''), 'name' : myarticle.readline().replace('#','') })
          
      except IOError:
        pass

  app.logger.debug(all_articles)

  all_articles.sort(key=lambda x: x['date'], reverse=True)

  

  # temp_return = ""

  # for full_file_path, file, article in all_articles:
  #   temp_return = temp_return + "<a href='" + pages_path + file + "'>" + article.replace("#","") + "</a>" + "<br>" 

  return render_template('index.html', articles=all_articles)

@app.route("/pages/<article>")

def show_page(article):
  # parsing code goes here
  title = ""
  content = ""

  article_url = url_for('static', filename=pages_path + article + '.md') 
  try:
    with open(pages_directory + article + ".md", 'r') as myarticle:
      file_content = myarticle.read()
  except IOError:
    abort(404)

  app.logger.debug(file_content)
  return render_template('pages.html', title=file_content.split('\n', 1)[0].replace("#",""), content=file_content)

@app.route("/pages/<article>/edit")

def edit_page(article):

  return "cool"