# get base image
FROM python:2.7-alpine

# copy flask app to app folder
COPY ./techtrends/ /app/

# set workdir
WORKDIR /app

# install requirements and initialize db
RUN pip install -r requirements.txt
RUN python init_db.py

# expose application port 3111
EXPOSE 3111

# run application
CMD [ "python", "app.py" ]