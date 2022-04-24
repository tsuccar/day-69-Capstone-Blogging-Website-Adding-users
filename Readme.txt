1) Starting File provided.

2) CKEditor did not install properly.

    Useful Docs: CKEditor Refresher and also in day-67 lesson

            https://flask-ckeditor.readthedocs.io/en/latest/basic.html

            https://pythonhosted.org/Flask-Bootstrap/forms.html

            https://flask-wtf.readthedocs.io/en/stable/

    install : pip install flask-ckeditor
              pip install flask-Gravatar
              pip install Werkzeug
              pip install Flask-WTF
              pip install flask-login
              pip install email-validator separately
              pip install Flask-Gravatar

3) In order to get 'user_login' module working, need the following steps.

        i) Make sure User(UserMixin,db.Model) is created with UserMixin so the appropriate functions are created.
        ii) refresh on https://flask-login.readthedocs.io/en/latest/
            need the following
                  1)  -from flask_login import LoginManager
                  2)  -login_manager = LoginManager()

                  3)  -login_manager.init_app(app)

                  4)  -@login_manager.user_loader
                        def load_user(user_id):
                            return User.query.get(int(user_id))       #<- turn str to int

                  5)  -login_user(user)                     #<- to authenticate
                      -logout_user()                        # <- to logout

                    -@login_required                        #<- above routes that require them

4) In order to user Login state Flash messages:

                1) https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
                2)
                3) in the HTML file
                       {% with messages = get_flashed_messages() %}
                            {% if messages %}
                             <ul class=flashes>
                                 {% for message in messages %}
                                    <li>{{ message }}</li>
                                  {% endfor %}
                             </ul>
                            {% endif %}
                        {% endwith %}

5) How to influence Nav Bar according to user-authenticated status:

               1) https://flask-login.readthedocs.io/en/latest/#login-example
               2)  current_user.name  : is available in every template
                                        for nav bar, it could be conveniently located in header.html
                         {% if current_user.is_authenticated %}
                              Hi {{ current_user.name }}!
                                    {% endif %}

6) How to protect Routes and give access to admin or certain user IDs.
    1. The first user's id is 1. We can use this in index.html and post.html
    to make sure that only the admin user can see the "Create New Post" and "Edit Post"
    and Delete buttons.

                        {% if current_user.id == 1: %}
                            <a href="{{url_for('delete_post', post_id=post.id) }}">✘</a>
                         {% endif %}

7) Python decorator called @admin_only
            If the current_user's id is 1 then they can access those routes, otherwise,
            they should get a 403 error (not authorised).

            HINT 1: You might need to review the lessons on Python Decorators on day 54.

HINT 2: See what the @login_required decorator looks like:
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/#login-required-decorator

HINT 3: The abort function is quick way to return HTTP errors like 403 or 404:
    https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/


8) Creating Relational Databases

    In relational databases such as SQLite, MySQL or Postgresql we're able to define a relationship
    between tables using a ForeignKey and a relationship() method.

     If we wanted to create a One to Many relationship between the User Table and the BlogPost table,
     where One User can create Many BlogPost objects, we can use the SQLAlchemy docs to achieve this.

    https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html

                        from flask_sqlalchemy import SQLAlchemy
                        from sqlalchemy.orm import relationship
                        from sqlalchemy import Table, Column, Integer, ForeignKey
                        from sqlalchemy.ext.declarative import declarative_base

                        Base = declarative_base()

    DB relationshiop example from one of the students:
    https://github.com/SadSack963/day-69_blog_with_users/blob/master/docs/Class_Diagram.png

    Best Parent/Child relationship is explained in :
    https://www.youtube.com/watch?v=VVX7JIWx-ss

9) Use the Gravatar docs here to add Gravatar images into your comments section.
    Docs : https://pythonhosted.org/Flask-Gravatar/

10) homework: Make the @login_required decorator work for log_out function.

11) To deploy on Heroku:

        - pip  install unicorn
        - Add the version in requirements.txt
         - project top-level folder called just - Procfile   <- no extention and 'P'
         - in the Procfile :  web: gunicorn main:app   : To use gunicorn to serve your
         web app and the Flask app object is the main.py file.

 12) At the time this is deployed Gihub is disabled on Heroku.
    Install Heroku client locally and uplode using git.
    https://devcenter.heroku.com/articles/git

        1) Intall Heroku :
            - brew tap heroku/brew && brew install heroku

       2)  Login:
            - heroku login

       3) Create a Heroku Remote:
            - heroku git:remote -a example-app      #remote-app mayhave been created in a browser
s               > et git remote heroku to https://git.heroku.com/example-app.git

       4) confirm with a command:
            - git remote -v
                > heroku  https://git.heroku.com/example-app.git (fetch)
                > heroku  https://git.heroku.com/example-app.git (push)

       5) for existing app on local machine:
            - heroku git:remote -a example-app
                > set git remote heroku to https://git.heroku.com/example-app.git

       6) deploy your code:
            - git push heroku main

       7) Reset a Git repo:
            - heroku repo:reset --app appname

       8) Repos size (<1GB)
            - heroku apps:info

 13) if you're using postgress DB, then

    SQLite is pre-installed for all Python projects, but if we are going to use
    Postgres, we'll need to install the psycopg2-binary packages as well. Note,
    you'll also need to add the package name and version to requirements.txt as
     well as commit and push the updates.
    -Psycopg is the most popular PostgreSQL database adapter for the Python programming language
        https://pypi.org/project/psycopg2-binary/
     -  pip install psycopg2-binary