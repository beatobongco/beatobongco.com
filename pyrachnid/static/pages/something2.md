# hello
please go vertigo
should be newline

newline

yeah

```python
from flask import Blueprint, render_template, redirect, url_for, abort
from app import app 

import os
from operator import itemgetter

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
    if file.endswith(".md"):
      try:
        with open(pages_directory+file, 'r') as myarticle:
          app.logger.debug("!")
          all_articles.append([pages_directory + file, file.replace('.md',''), myarticle.readline()])
          all_articles.sort(key=lambda x: os.path.getmtime(x[0]), reverse=True)
      except IOError:
        pass

  app.logger.debug(all_articles)
  temp_return = ""

  for full_file_path, file, article in all_articles:
    temp_return = temp_return + "<br>" + "<a href='" + pages_path + file + "'>" + article + "</a>"

  return render_template('pages.html', title="Your Site's Name", content=temp_return)

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

  return render_template('pages.html', title=title, content=file_content)

@app.route("/pages/<article>/edit")

def edit_page(article):

  return "cool"```

Lorem ipsum dolor sit amet, consectetur adipiscing elit. In aliquam lacinia risus, vel congue felis tincidunt sed. Pellentesque enim dolor, blandit vitae metus eget, sagittis gravida elit. Aenean vitae sapien odio. Pellentesque leo urna, commodo in magna at, lacinia rhoncus augue. Vivamus vitae lacus mattis, lacinia nunc mattis, pretium purus. Nunc sit amet sapien eu erat porta facilisis. Quisque dictum rutrum libero et hendrerit.

Quisque eu luctus dui. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Morbi rutrum, velit ac imperdiet aliquet, sem felis eleifend magna, at blandit risus mi non ante. Aenean fringilla vulputate nisl sit amet sagittis. Pellentesque molestie, dolor eget tempus lobortis, mi neque mattis eros, non molestie justo risus vitae magna. Fusce convallis lobortis pellentesque. Donec mauris ipsum, imperdiet et urna vel, viverra pretium quam. Sed ultrices nisi vitae eleifend sodales. Sed sodales urna risus, quis fermentum risus facilisis eget. Maecenas vel dolor eget risus consectetur accumsan. Nulla neque ante, tincidunt in nisl at, hendrerit euismod mauris.

Quisque auctor, libero ut volutpat euismod, tellus augue sollicitudin leo, at interdum orci velit quis nulla. Duis sagittis et sem sit amet mattis. Mauris eu auctor orci. Donec auctor placerat nisi, quis ultricies est placerat a. Nam eleifend lacinia ipsum, ac sollicitudin augue luctus non. Ut sit amet enim est. Sed tristique imperdiet magna ac suscipit. Maecenas non tempor augue, eget consectetur elit. Nam id libero elementum neque ultricies condimentum. Maecenas tempus rutrum libero, at malesuada elit sagittis id. Pellentesque posuere, lacus et sodales porta, felis tellus dapibus lectus, eget vehicula diam purus eget lacus. Praesent nec massa nec nulla ultrices feugiat. Nunc bibendum, neque et volutpat ultrices, ante risus vulputate felis, eu tristique nisi justo vitae erat. Morbi quis pellentesque magna, sed suscipit massa.

Curabitur at nisl sodales, placerat dolor a, pulvinar dui. Pellentesque adipiscing placerat accumsan. Maecenas eleifend porta laoreet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Donec vestibulum, velit aliquam feugiat tempor, est tortor convallis neque, dapibus dapibus nisi lectus a leo. Ut risus mauris, pellentesque ut ultricies mattis, fringilla non neque. Maecenas ac lectus eleifend, convallis nulla vitae, tincidunt enim. Donec dolor tortor, rhoncus sed interdum in, gravida eget quam.

Ut porta, lorem eu adipiscing commodo, elit mauris suscipit diam, in iaculis ipsum metus ut mauris. Donec ut dui lacus. Quisque viverra dui at lorem lacinia, eget vestibulum augue aliquet. Nam condimentum massa augue. Curabitur porta enim vel dictum gravida. Curabitur vitae dolor dui. Fusce quis faucibus lectus. Curabitur fermentum felis odio, ac auctor dolor tincidunt vitae. Proin cursus, ante viverra volutpat porttitor, nibh dolor ornare purus, non euismod lectus lorem nec velit. Mauris nec mollis leo. Aliquam at iaculis nulla.