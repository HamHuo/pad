FROM tiangolo/uwsgi-nginx:python3.5

MAINTAINER Trim21 <Trim21me@gmail.com>

RUN pip install flask werkzeug jinja2 peewee flask-peewee

# Add app configuration to Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Copy sample app
COPY ./app /app


