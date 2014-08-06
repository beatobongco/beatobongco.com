from flask import Blueprint, render_template, redirect, url_for
from app import app 

import os

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

  with open(full_directory + article_url, 'r') as myarticle:
    file_content = myarticle.readlines()

  title = file_content[0]
  content= '<br>'.join(file_content[1:]).replace('<img src="','<img src="../static/img/')

  return render_template('pages.html', title=title, content=content)