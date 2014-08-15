# How to set up nginx, gunicorn and flask on a fresh server

## Preparation 

1. ```sudo apt-get update```

2. `sudo apt-get install python-dev`

3. `sudo apt-get install python-setuptools`

4. `sudo easy_install -U pip`


## Install virtualenvwrapper 

_Optional_: You can do ```export PATH=$PATH:~/.local/bin``` so that you won't need to use sudo priveleges.

1. `sudo pip install virtualenvwrapper`   

2. `nano .bashrc` and add the following line at the end `source virtualenvwrapper.sh`  

3. `source .bashrc` or `. .bashrc` to reload your `.bashrc` file 


## How to install Nginx

`sudo apt-get install nginx`

### Some useful commands for Nginx

* `sudo service nginx start`
* `sudo service nginx stop`

After each time you reconfigure Nginx, a restart or reload is needed for the new settings to come into effect.

* `sudo service nginx restart`
* `sudo nginx -s reload`

## How to configure Nginx

1. `sudo nano /etc/nginx/conf.d/<somename>.conf`

2. Paste this and save

    ```python
    server {
        listen 80;

        server_name your server name here;

        access_log  /var/log/nginx/access.log;
        error_log  /var/log/nginx/error.log;

        location / {
            proxy_pass         http://127.0.0.1:8000/;
            proxy_redirect     off;

            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        }
    }
    ```

3. `sudo nginx -s reload`

## Make a virtualenv

1. `mkvirtualenv <your virtual env name>`

2. To work on a virtualenv do `workon <your virtual env name>`

## Install Flask

`pip install flask`

Flask tips will be covered in another post.

## How to update the website:

1. Go to the directory where your app is located. Work on your virtual env

    `workon <your virtual env>`

2. Then, we kill gunicorn.

    `pkill gunicorn`

3. Then we `git clone` or `git pull` the flask app.

4. Then we run gunicorn.

    `gunicorn -b 0.0.0.0:5000 -D pyrachnid.app:app`

5. ??? Profit!


