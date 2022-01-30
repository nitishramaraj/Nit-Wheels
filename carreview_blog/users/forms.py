
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Email, EqualTo, DataRequired
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from carreview_blog.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        username = StringField('User-Name', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match')])
        pass_confirm= PasswordField('Confirm Password', validators=[DataRequired()])
        submit= SubmitField('Register')

        def check_email(self,field):
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('You email is already registered with us!')
                
        def check_username(self,field):
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username is already in use!')


class UpdateUserForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('User-Name', validators=[DataRequired()])
    picture = FileField('Update your Display Picture', validators=[FileAllowed(['jpg','png'])])
    submit= SubmitField('Update')

    def check_email(self,field):
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('You email is already registered with us!')
                
    def check_username(self,field):
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username is already in use!')


    

                                                                            