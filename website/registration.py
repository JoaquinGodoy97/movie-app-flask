from flask import Blueprint, render_template, request, url_for, redirect

registration = Blueprint('registration', __name__)

@registration.route('/', methods=['GET', 'POST'])
def main_page():

    if 'email_submit' in request.form:
        return redirect(url_for('home.search'))

    return render_template('registration.html')

