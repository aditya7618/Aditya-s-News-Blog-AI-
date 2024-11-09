from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
 

# Load configuration
local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)['params']

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Configure database URI
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Post model (table)
class Post(db.Model):
    __tablename__ = 'posts'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, nullable=False)
# Route for the home page
@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("index.html", params=params, posts=posts)


# Route for login handling both GET and POST methods
@app.route("/login", methods=["GET", "POST"])
def login():
    if('user' in session and session['user']==params['admin_user']):
       
        return render_template("dashboard .html", params=params)
    # Handle GET request - show the login page
    if request.method == "GET":
        return render_template("login page .html", params=params)

    # Handle POST request - process the login
    elif request.method == "POST":
        username = request.form.get("uname")
        userpass = request.form.get("password")
        

        # Check credentials
        if username == params["admin_user"] and userpass == params["admin_password"]:
            session["user"] = username
            posts=Post.query.all()
            print("Login successful")  # Debug output
            return render_template("dashboard .html", params=params,post=posts)
        else:
            print("Invalid credentials")  # Debug output
            return render_template("login page .html", params=params, error="Invalid credentials")


# Route for viewing a specific post
@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    return render_template("post page.html", params=params, post=post)

# Route for managing categories
@app.route("/managecategories")
def manage_categories():
    return render_template("manage categories.html", params=params)

# Route for managing posts
@app.route("/managepost/<string:sno>", methods=['GET', 'POST'])
def managepost(sno):
    if('user' in session and session['user']==params['admin_user']):
        if request.method=="POST":
            box_title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')
            date = datetime.now() 
            if sno=="0":
                post=Post(title=box_title, slug=slug,content=content,date=date)
                db.session.add(post)
                db.session.commit()
        return render_template("Add Post.html", params=params,sno=sno)

# Route for managing tags
@app.route("/postmanagement")
def postmanagement():
    if('user' in session and session['user']==params['admin_user']):
        posts=Post.query.all()
        return render_template("postmanagement.html", params=params,posts=posts )

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
