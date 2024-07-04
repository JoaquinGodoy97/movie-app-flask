from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from website.utils.db import db
from .models.user import User

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

            if found_user.password == password:
                print(found_user.password)
                flash(f"Welcome back {user}", "success")
                return redirect(url_for("homepage.search"))
            
            
            elif not password:
                print('missing password/email')
                flash("Please insert a password", "warning")
                return redirect(url_for('auth.logout'))
            
            else:
                flash(f"Invalid Password", "danger")
                return redirect(url_for('auth.logout'))
            
            return redirect(url_for('auth.index'))

        else:

            if not password:
                print('missing password/email')
                flash("If you are new please insert a password", "warning")
                return redirect(url_for('auth.index'))
            
            session['username'] = user
            user_db = User(user, email, password)
            db.session.add(user_db)
            db.session.commit()
            flash(f"You've logged in as {session['username']}. Please don't forget your password is {password}", "success")
            return redirect(url_for('homepage.search'))

        
    return redirect(url_for("auth.index"))

@auth.route('/logout')
def logout():
    if 'username' in session:
    # remove the username from the session if it's there
        # flash(f'{session['username']} has been logged out', "dark")
        session.pop('username', None)
    
    return redirect("auth")