from util import now
from app import db

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(), unique=True)
  title = db.Column(db.String(), unique=True)
  body = db.Column(db.String())
  category = db.Column(db.String())
  image = db.Column(db.String())
  preview = db.Column(db.String())
  created = db.Column(db.Integer)
  modified = db.Column(db.Integer)

  def __init__(self, url, title, preview, category, body, image=None):
    self.url = url
    self.title = title
    self.body = body
    self.category = category
    self.created = now()
    self.preview = preview
    self.image = image

  def __repr__(self):
    return '<Post %r>' % self.url