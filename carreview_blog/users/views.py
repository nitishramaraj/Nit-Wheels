
from fileinput import filename
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from carreview_blog import db, login_manager
from carreview_blog.models import User, BlogPost
from carreview_blog.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from carreview_blog.users.picture_handler import add_profile_pic
import stripe

users= Blueprint('users',__name__)


#register
@users.route('/register', methods=['GET','POST'])
def register():
    form= RegistrationForm()

    if form.validate_on_submit():
        user= User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data
                   )
        db.session.add(user)
        db.session.commit()
        flash('You are now registered with us')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)    

#login
@users.route('/login', methods=['GET','POST'])
def login():

    form=LoginForm()
    if form.validate_on_submit():

        user= User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('You are now logged in')

            next= request.args.get('next')

            if next == None or not next[0]=='/':
                next= url_for('core.home')

            return redirect(next)    

        elif not user.check_password(form.password.data):
            flash('The entered password is incorrect')    

    return render_template('login.html', form=form)

#logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.home"))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))
        


    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):
    page=request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts= BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)


