from flask import render_template, request, redirect, url_for, flash
from app.blueprints.auth.forms import LoginForm, SignUp, EditProfile
from app.blueprints.auth import auth
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        
        # Query user from db
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully Logged In! Welcome back, {queried_user.first_name}!', 'success')            
            return redirect(url_for('main.home'))
        else:
            error = 'Incorrect Email/Password!'
            flash(f'{error}', 'danger')
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)

@auth.route('/signup', methods=['Get', 'POST'])
def signup():
    form = SignUp()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }
        new_user = User()

        # Implementing values from our form data for our instance
        new_user.from_dict(new_user_data)

        # Save user to database
        new_user.save_to_db()

        flash('You have successfully registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfile()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
        }

        #query User from db to change by email
        queried_user = User.query.filter_by(email=new_user_data['email']).first()
        if queried_user:
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.editprofile'))
        else:
            #add changes to db
            current_user.update_from_dict(new_user_data)
            current_user.save_to_db()
            flash('Profile updated!', 'success')
            return redirect(url_for('main.home'))

    return render_template('editprofile.html', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'warning')
        return redirect(url_for('auth.login'))