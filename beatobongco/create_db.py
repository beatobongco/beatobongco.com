from app import db
from models import Post

db.create_all()

test = Post(
  "hello", 
  "Hello, World!", 
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 
  "blog, life",  
  '''Sometimes the world isn't ready for some shit.  
  I mean, seriously, come on.  
  Third Line.  
  Fourth.  
  Fifth.  ''',
  "http://fillmurray.com/200/300"
  )

test2 = Post(
  "hello2", 
  "Hello, World 2!", 
  "A simple test post.", 
  "blog, life",  
  '''Sometimes the world isn't ready for some shit.  
  I mean, seriously, come on.  
  Third Line.  
  Fourth.  
  Fifth.  ''',
  "http://fillmurray.com/1000/642"
  )

test3 = Post(
  "hello3", 
  "Hello, World 3!", 
  "A simple test post.", 
  "blog, life",  
  '''Sometimes the world isn't ready for some shit.  
  I mean, seriously, come on.  
  Third Line.  
  Fourth.  
  Fifth.  ''',
  "http://fillmurray.com/200/1000"
  )

test4 = Post(
  "hello4", 
  "Hello, World 4!", 
  "A simple test post.", 
  "blog, life",  
  '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.''',
  "http://fillmurray.com/1366/768"
  )

db.session.add(test)
db.session.add(test2)
db.session.add(test3)
db.session.add(test4)

db.session.commit()