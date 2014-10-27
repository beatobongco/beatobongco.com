from app import db
from models import Post

db.create_all()

test = Post(
  "hello", 
  "Hello, World!", 
  "A simple test post.", 
  "blog, life",  
  '''Sometimes the world isn't ready for some shit.  
  I mean, seriously, come on.  
  Third Line.  
  Fourth.  
  Fifth.  ''',
  "http://localhost:4000/static/img/test-all-the-things.jpg"
  )

db.session.add(test)
db.session.commit()