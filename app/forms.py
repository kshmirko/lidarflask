import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField, FileField

from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import db
import sqlalchemy as sa
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me=BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username==username.data))
        if user is not None:
            raise ValidationError('Please use different username')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use differen email')

    
from wtforms import TextAreaField
from wtforms.validators import Length

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    

from wtforms import DateTimeLocalField, DateField

class UploadForm(FlaskForm):
    experiment_title = StringField('Название:', validators=[DataRequired(), Length(min=10, max=100)])
    experiment_descr = TextAreaField('Описание:', validators=[DataRequired(), Length(min=10, max=512)])
    experiment_date = DateField('Дата проведения:')
    spatial_res = FloatField('Шаг вдоль луча (метры):', validators=[DataRequired(), NumberRange(min=1500, max=1912.5)])
    accum_time = FloatField('Время накопления (минуты):', validators=[DataRequired(), NumberRange(min=0, max=120)])
    experiment_file_dat = FileField('Архив с данными DAT:', validators=[FileAllowed(['zip']), FileRequired()])
    experiment_file_dak = FileField('Архив с данными DAK:', validators=[FileAllowed(['zip']), FileRequired()])
    submit = SubmitField('Отправить')

