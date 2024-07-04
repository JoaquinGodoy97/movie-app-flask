from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import requests, json

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/wishlist', methods=["POST", "GET"])
def wishlist_page():
    # flash('hola mundo', 'warning')

    if request.method == 'POST':




        #LOG OUT

        if request.form.get('logout') == 'Log Out':
            flash(f"{session['username']} has been logged out", "dark")
            return redirect(url_for('auth.logout'))
    else:

        #CHECK FOR USER IN SESSION

        if "username" not in session:
            return redirect(url_for('auth.logout'))
    
    return render_template('wishlist.html')