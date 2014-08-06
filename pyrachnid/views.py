from flask import Blueprint, render_template, redirect, url_for, abort
from app import app 

import os

#Variables
static_directory = os.path.dirname(os.path.abspath(__file__)) + "/static/"
pages_path = "pages/"
pages_directory = static_directory + pages_path

replacement = [ 
  ['[b]' , '<b>'],
  ['[/b]' , '</b>'],
  ['[u]' , '<u>'],
  ['[/u]' , '</u>'],
  ['[i]' , '<i>'],
  ['[/i]' , '</i>'],
  ['[/img]' , '">'],
  ['[img]' , '<img src="'],
  ['[img2]' , '<img style="width: 50%; height: 50%" src="'],
  ['[img3]' , '<img style="width: 25%; height: 25%" src="'],
  ['[iimg]' , '<img src="../static/img/'],
  ['[iimg2]' , '<img style="width: 50%; height: 50%" src="../static/img/'],
  ['[iimg3]' , '<img style="width: 25%; height: 25%" src="../static/img/'],
  ['[/iimg]' , '">'],
  ['  ' , '&nbsp;&nbsp;'],
  ['[/' , '</'],
]

# Functions

#Dict for replacement
def replace_all(text, dic):
  for i, j in replacement:
    text = text.replace(i, j)
  return text

@app.route("/")

def index():
  # get all titles of blog entries
  all_articles = []

  for file in os.listdir(pages_directory):
    if file.endswith(".txt"):
      try:
        with open(pages_directory+file, 'r') as myarticle:
          app.logger.debug("!")
          all_articles.append([file.replace('.txt', ''), myarticle.readline()])
      except IOError:
        pass

  app.logger.debug(all_articles)
  temp_return = ""

  for file, article in all_articles:
    temp_return = temp_return + "<br>" + "<a href='" + pages_path + file + "'>" + article + "</a>"

  return render_template('pages.html', title="Your Site's Name", content=temp_return)

@app.route("/pages/<article>")

def show_page(article):
  # parsing code goes here
  title = ""
  content = ""

  article_url = url_for('static', filename='pages/' + article + '.txt') 
  try:
    with open(pages_directory + article + ".txt", 'r') as myarticle:
      file_content = myarticle.readlines()
  except IOError:
    abort(404)

  try:
    title = file_content[0]
  except IndexError:
    title = "There's nothing here."

  content = replace_all('<br>'.join(file_content[1:]), replacement)

  return render_template('pages.html', title=title, content=content)