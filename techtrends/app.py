import sqlite3
import logging
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# initialize db_connection_count
db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        logging.error("Article {} does not exist!".format(post_id))
        return render_template('404.html'), 404
    else:
        logging.info('Article "{}" retrieved!'.format(post['title']))
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logging.info('About page retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            logging.info('Article "{}" created!'.format(title))
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the healthz endpoint
# Extend the /healthz endpoint to return a 500 HTTP ERROR - unhealthy error 
# if the connection to the database fails or if the required posts table does not exist.
# To validate your endpoint, try deleting the database.db file and check if the endpoint is returning a 500 error.
@app.route('/healthz', methods=['GET'])
def healthz():
    try:
        connection = get_db_connection()
        posts = connection.execute('SELECT * FROM posts').fetchall()
        connection.close()
        response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
        )
    except Exception:
        response = app.response_class(
        response=json.dumps({"result":"ERROR - unhealthy"}),
            status=500,
            mimetype='application/json'
        )
    
    return response

# Define the metrics endpoint
# returns Total amount of posts in the database and
#         total amount of connections to the database. For example, accessing an article will query the database, hence will count as a connection.
@app.route('/metrics', methods=['GET'])
def metrics():
    connection = get_db_connection()
    posts_count = connection.execute('SELECT count(*) FROM posts').fetchone()
    connection.close()
    response = app.response_class(
            response=json.dumps({"db_connection_count": db_connection_count, "post_count": posts_count[0]}),
            status=200,
            mimetype='application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
    # logger code snippet from https://knowledge.udacity.com/questions/612353
    logger = logging.getLogger("__name__")
    
    h1 = logging.StreamHandler(sys.stdout)
    h1.setLevel(logging.DEBUG)
    h2 = logging.StreamHandler(sys.stderr)
    h2.setLevel(logging.ERROR)
    logger.addHandler(h1)
    logger.addHandler(h2)
    # format from https://docs.python.org/3/howto/logging.html
    logging.basicConfig(level=logging.DEBUG,
        format='%(levelname)s:%(name)s - %(asctime)s, %(message)s', handlers=[h1,h2])
    app.run(host='0.0.0.0', port='3111')
