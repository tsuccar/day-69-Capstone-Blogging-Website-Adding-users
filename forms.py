from flask_wtf import FlaskForm                                  # pip install flask-WTF
#  and Fields that along with WTForm
from wtforms import StringField, SubmitField, PasswordField
#  and their validators <--                                      installed pip install email-validator separately
from wtforms.validators import DataRequired, URL, Email,Length           # pip install email-validator
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

## usedd to register from form
class RegisterForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=2)])
    name = StringField(label='Name', validators=[DataRequired()])
    submit = SubmitField(label="Sign me up!")
    
## used to log in the user
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Log me in!")
    
## used to log in the user
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField(label="Submit Comment")