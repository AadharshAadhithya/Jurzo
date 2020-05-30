from flask import render_template, request,  redirect, flash, url_for, Blueprint
from Jurzo import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from Jurzo.models import User, Page
from Jurzo.users.fourms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from Jurzo.users.utils import send_reset_email\

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    forms = RegistrationForm()
    if current_user.is_authenticated:
        return redirect('home')
    if forms.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            forms.password.data).decode('utf-8')
        user = User(username=forms.username.data,
                    password=hashed_pass, email=forms.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Acount has been succesfully created for {},You can now login.".format(
            forms.username.data), category="success")
        return redirect(url_for('users.login'))

    return render_template('register.html', forrm=forms)


@users.route('/login', methods=['GET', 'POST'])
def login():
    forms = LoginForm()
    if current_user.is_authenticated:
        return redirect('home')
    if forms.validate_on_submit():
        user = User.query.filter_by(username=forms.username.data).first()
        if user and bcrypt.check_password_hash(user.password, forms.password.data):
            login_user(user, remember=forms.remember_me.data)
            next_page = request.args.get('next')
            return redirect((next_page)) if next_page else redirect(url_for('main.home'))

        else:
            flash("login uncessfull",  category='danger')
    return render_template('login.html', forrm=forms)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/memoirs')
@login_required
def memoirs():
    pages = Page.query.filter_by(
        owner=current_user).order_by(Page.date_created.desc())
    Quotes = []
    From = []
    for page in pages:
        Quotes.append(page.Quote)
        From.append(page.name)
    Front_Content = {Quotes[i]: From[i] for i in range(len(Quotes))}

    return render_template('memoirs.html', pages=pages, Quotes=Front_Content)


@users.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An link has been sent to your email to reset")
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)


@users.route("/reset_password/<token>", methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'Warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_pass
        db.session.commit()
        flash("Password has been updated {},You can now login.".format(
            user.username), category="success")
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', form=form)
