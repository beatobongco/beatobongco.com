# How to set up nginx, gunicorn and flask in a fresh server

## Preparation 

1. `sudo apt-get update`

2. `sudo apt-get install python-dev`

3. `sudo apt-get install python-setuptools`

4. `sudo easy_install -U pip`

5. Install virtualenvwrapper  

## How to install virtualenvwrapper 

1. `pip install virtualenvwrapper` 

You can also `pip install --local virtualenvwrapper` to install without sudo priveleges. 

2. `nano .bashrc` and add the following line at the end `source virtualenvwrapper.sh`

3. `source .bashrc` or `. .bashrc` to reload your `.bashrc` file 


## How to make a virtualenv

1. `mkvirtualenv <your virtual env name>`

2. To work on a virtualenv do `workon <your virtual env name>`

## How to install Nginx

`sudo apt-get install nginx`

## Some useful commands for Nginx

* `sudo service nginx start`
* `sudo service nginx stop`

After each time you reconfigure Nginx, a restart or reload is needed for the new settings to come into effect.

* `sudo service nginx restart`

## How to configure Nginx

1. sudo nano /etc/nginx/conf.d/<somename>.conf

2. Paste this and save

```
server {
    listen 80;

    server_name _;

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

3. sudo nginx -s reload

## How to update the website:

1.  First, we kill gunicorn.

`pkill gunicorn`

2. Then we git pull.

3. Then we run gunicorn.

`gunicorn -b 0.0.0.0:5000 -D pyrachnid.app:app`


