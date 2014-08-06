from flask import Blueprint, render_template, redirect, url_for, abort
from app import app 

import os

# Functions

#Dict for replacement
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

def replace_all(text, dic):
  for i, j in replacement:
    text = text.replace(i, j)
  return text

@app.route("/")

def index():
  return "Hello World!!"

@app.route("/pages/<article>")

def show_page(article):
  # parsing code goes here
  full_directory = os.path.dirname(os.path.abspath(__file__))
  title = ""
  content = ""

  article_url = url_for('static', filename='pages/' + article + '.txt') 
  try:
    with open(full_directory + article_url, 'r') as myarticle:
      file_content = myarticle.readlines()
  except IOError:
    abort(404)

  try:
    title = file_content[0]
  except IndexError:
    title = "There's nothing here."

  content = replace_all('<br>'.join(file_content[1:]), replacement)

  return render_template('pages.html', title=title, content=content)