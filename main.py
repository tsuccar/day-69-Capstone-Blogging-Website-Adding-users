from flask import Flask, render_template, redirect, url_for, flash,request,abort,g
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
### for password hashing and checking
from werkzeug.security import generate_password_hash, check_password_hash
# DB related
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer
# The following will keep track of the user logged and in session with the help of secure cookie
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# Locally imported file that has all flas-WTF, fields and validators
from forms import CreatePostForm,RegisterForm,LoginForm,CommentForm
from flask_gravatar import Gravatar       # pip install flask-gravatar
from functools import wraps
# for environment config
import os

app = Flask(__name__)
# the SECRET_KEY was supplied on Heroku config vars in settings.
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# works with flask-login                https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.init_app(app)

##CONNECT TO DB
# this  DTABASE_URL setting will be activated for postgress db URL if it is deployed on Heroku. it
# it fails then goes back to using sqlite locally

# on Herooku chnaged the URL name from postgres to postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL2","sqlite:///blog.db")
#"sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLES
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email =  db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    #This will act like a List of BlogPost objects attached to each User.
    #The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost",back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")
# Line below only required once, when creating DB.
# db.create_all()

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    #Create Foreign Key, "user.id" the users refers to the tablename of the User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = relationship("User", back_populates="posts")       #Author now is a User object instead of name.
    comments = relationship("Comment", back_populates="parent_post")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

# 'comments' is a property of each blog post, you can treat it like a List
#  The text of each comment is created from the CKEditor just like the body of each blog post so it will be saved in HTML format.


#Line below only required once, when creating DB.
# db.create_all()

##CONFIGURE TABLES
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    # ***************Child Relationship*************#
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text = db.Column(db.Text, nullable=False)
#Line below only required once, when creating DB.
# db.create_all()

# following is a call back to lookin into the session DB to retrieve
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))       #<- from str to int since DB requires int but loader string


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('login', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

@app.route('/')
#Mark with decorator
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)

# Interesting obeservation here. register_form is facilitating both on
# HTML FORM rendering  incoming request as well
@app.route('/register',methods=['GET','POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if not User.query.filter_by(email=register_form.email.data).first():
            print("it's not in the database")
            new_user = User(
                name = register_form.name.data,
                email = register_form.email.data,
                password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256',salt_length=8)
            )
            db.session.add(new_user)
            db.session.commit()
            # authenticated
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
        else:
            flash("You have already have an account, please log in !")
            return redirect(url_for("login"))
    return render_template("register.html",form=register_form)

@app.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user:
            if check_password_hash(user.password,login_form.password.data):
                # authenticated
                login_user(user)
                return redirect(url_for("get_all_posts"))
    return render_template("login.html",form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>",methods=['GET','POST'])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    
    
    return render_template("post.html", post=requested_post,form=form,current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post",methods=['GET','POST'])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,                # this one didn't necessarity come from the form
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>",methods=['GET','POST'])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form,is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
