from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from website.utils.db import db
from .models.user import User
import re

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        return render_template("auth.html")

    else:
        if 'username' in session:
            # session.pop('username', None)
            print(f'Logged in as {session["username"]}')
            return redirect(url_for("homepage.search"))
        
        print("No username in session!")
        return render_template("auth.html")



@auth.route('/auth', methods=['GET', 'POST'])
def login():

    password_check = r"^[A-Za-z0-9]{5,9}$"

    if request.method == 'POST':
        session.permanent = True
        user = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        found_user = User.query.filter_by(username=user).first()

        if found_user: # If found in DB

            # if not email:
            #     print('missing password/email')
            #     flash("no email/password")
            #     return redirect(url_for('auth.index'))

            print(found_user)
            print(f"user already in database.")

            session['username'] = user

            if re.match(password_check, password):

                if found_user.password == password:
                    print(found_user.password)
                    flash(f"Welcome back {user}", "success")
                    return redirect(url_for("homepage.search"))

                else:
                    
                    print('missing password/email')
                    flash("Please insert a valid password", "danger")
                    return redirect(url_for('auth.logout'))

            else:
                flash(f"Invalid Password. Write a password between 5-9 characters long no spaces.", "danger")
                return redirect(url_for('auth.logout'))

            return redirect(url_for('auth.index'))

        else:

            if re.match(password_check, password):

                session['username'] = user
                # user_db = User(user, email, password)
                # db.session.add(user_db)
                # db.session.commit()

                try:
                    user_db = User(user, email, password)
                    db.session.add(user_db)
                    db.session.commit()
                    flash(f"You've logged in as {session['username']}. Please don't forget your password is {password}", "success")
                    return redirect(url_for('homepage.search'))
                except Exception as e:
                    db.session.rollback()
                    flash(f"An error occurred while saving to the database: {str(e)}", "danger")
                finally:
                    db.session.close()
            else:
                print('missing password/email')
                flash("If you are new insert a invalid password. Write a password between 5-9 characters long no spaces.", "warning")
                return redirect(url_for('auth.index'))

    return redirect(url_for("auth.index"))

@auth.route('/logout')
def logout():
    if 'username' in session:
    # remove the username from the session if it's there
        # flash(f'{session['username']} has been logged out', "dark")
        session.pop('username', None)
    
    return redirect("auth")