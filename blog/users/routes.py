from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from blog.models import Post, User
from blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            RequestResetForm, ResetPasswordForm)
from blog import db, bcrypt 
from flask_login import login_user, current_user, logout_user, login_required
from blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username=form.username.data, email=form.email.data,password=hashed_password)
        user.save()
        flash(f'Account created for {form.username.data}. Then, you can login Now', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()  
    if form.validate_on_submit():
        user = User.objects.filter(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # flash(f'You have been logged in by {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Email or Password wrong. Please check again.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account(): 
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.save()
        flash(f'Your Account Have Been Updated', 'success') 
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                            image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username): 
    page = request.args.get('page', 1, type=int) 
    user = User.objects.get(username=username) 
    posts = Post.objects(author=user)\
                        .order_by('-date_posted')\
                        .paginate(page=page, per_page=2) 
    return render_template('user_posts.html',posts = posts, title='User Page',user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request(): 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm() 
    if form.validate_on_submit():
        user = User.objects.get_or_404(email=form.email.data)
        send_reset_email(user)
        flash('Email have been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',form =form, title='Reset Password Page')

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token): 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an valid or expired token', 'warning')
        return redirect(url_for(users.reset_request))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user.password = hashed_password
        user.save()
        flash(f'Your password have been updated! Then, you can login Now', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',form =form, title='Reset Password Page')

