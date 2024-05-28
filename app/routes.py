from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from app.forms import RegistrationForm, UploadForm
from app.models import User, Experiment, MeasurementCh1, MeasurementCh2
from urllib.parse import urlsplit
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from app.utils.lidar_file import LidarFile
import os
import json


from zipfile import ZipFile

def process_upload_form(form):
    print(form.experiment_title.data)
    print(form.experiment_descr.data)
    print(form.experiment_date.data)
    print(form.spatial_res.data)
    print(form.accum_time.data)
    #Add experiment
    start_time = datetime(form.experiment_date.data.year, form.experiment_date.data.month, form.experiment_date.data.day)
    exp = db.session.scalar(
        sa.select(Experiment).where(Experiment.start_time==start_time)
    )
    
    if exp is None:
        exp = Experiment()
        exp.start_time = datetime(form.experiment_date.data.year, form.experiment_date.data.month, form.experiment_date.data.day)
        exp.title = form.experiment_title.data
        exp.description = form.experiment_descr.data
        exp.accum_time = float(form.accum_time.data)
        exp.vert_res = float(form.spatial_res.data)
        db.session.add(exp)

    full_file_name_dat = os.path.join(app.config['UPLOAD_FOLDER'],form.experiment_file_dat.data.filename)
    form.experiment_file_dat.data.save(full_file_name_dat)
    print(full_file_name_dat)

    full_file_name_dak = os.path.join(app.config['UPLOAD_FOLDER'],form.experiment_file_dak.data.filename)
    form.experiment_file_dak.data.save(full_file_name_dak)
    print(full_file_name_dak)

    
    #read first channel A
    with ZipFile(full_file_name_dat) as myzip:
        for name in myzip.namelist():
            print(name)
            with myzip.open(name) as fin:
                lidarfile = LidarFile(fin)

                m = MeasurementCh1()
                m.start_time = lidarfile.start_time
                m.prof_len = len(lidarfile.data)
                m.count = lidarfile.count
                m.rep_rate = lidarfile.rep_rate
                m.prof_data = json.dumps(lidarfile.data)
                m.experiment = exp
                m.user = current_user
                db.session.add(m)
    

    #read channel b

    with ZipFile(full_file_name_dak) as myzip:
        for name in myzip.namelist():
            print(name)
            with myzip.open(name) as fin:
                lidarfile = LidarFile(fin)

                m = MeasurementCh2()
                m.start_time = lidarfile.start_time
                m.prof_len = len(lidarfile.data)
                m.count = lidarfile.count
                m.rep_rate = lidarfile.rep_rate
                m.prof_data = json.dumps(lidarfile.data)
                m.experiment = exp
                m.user = current_user
                db.session.add(m)
    try:
        db.session.commit()
    except:
        flash("Дубликат данных, транзакция отменена!")
        db.session.rollback()


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    
    return render_template('index.html', title='Home',  posts=posts)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
            
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username==username))
    posts = [
        {'author': user, 'body':'Test post #1'},
        {'author': user, 'body':'Test post #2'}
    ]    
    return render_template('user.html', user=user, posts=posts)

from app.forms import EditProfileForm

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    form=UploadForm()

    if form.validate_on_submit():
        process_upload_form(form)

    return render_template('upload_data.html', title='Upload data', 
                            form=form)
    
