
from flask import *
from Jurzo.fourms import RegistrationForm , LoginForm,PageForm,RequestResetForm,ResetPasswordForm
from Jurzo import jurzo
import pdfkit



from Jurzo.models import User, Page
from Jurzo import db,bcrypt,mail
from flask_login import  login_user,current_user,logout_user,login_required
from flask_mail import Message

@jurzo.route('/')
@jurzo.route('/home')
def home():
    return render_template('home.html', title='home',user=current_user )



@jurzo.route('/register',methods=['GET', 'POST'])
def register():
    forms = RegistrationForm()
    if current_user.is_authenticated:
        return redirect('home')
    if forms.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(forms.password.data).decode('utf-8')
        user = User(username=forms.username.data,password=hashed_pass, email= forms.email.data )
        db.session.add(user)
        db.session.commit()
        flash("Acount has been succesfully created for {},You can now login.".format(forms.username.data),category="success")
        return redirect(url_for('login'))

    return render_template('register.html', forrm=forms)



@jurzo.route('/login', methods=['GET', 'POST'])
def login():
    forms = LoginForm()
    if current_user.is_authenticated:
        return redirect('home')
    if forms.validate_on_submit():
        user = User.query.filter_by(username=forms.username.data).first()
        if user and bcrypt.check_password_hash(user.password,forms.password.data):
            login_user(user,remember=forms.remember_me.data)
            next_page=request.args.get('next')
            return redirect((next_page)) if next_page else redirect(url_for('home'))

        else:
            flash("login uncessfull",  category='danger')
    return render_template('login.html', forrm=forms)


@jurzo.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@jurzo.route('/memoirs')
@login_required
def memoirs():
    pages  = Page.query.filter_by(owner=current_user).order_by(Page.date_created.desc())
    Quotes =[]
    From = []
    for page in pages:
        Quotes.append(page.Quote)
        From.append(page.name)
    Front_Content = {Quotes[i] : From[i] for i in range(len(Quotes))}

    return render_template('memoirs.html' , pages = pages, Quotes = Front_Content )



@jurzo.route('/page/<username>',methods=['GET', 'POST'])
def page(username):
    owner = User.query.filter_by(username=username).first()
    forms=PageForm()
    if forms.validate_on_submit():
        page = Page(owner = owner ,name=forms.name.data , pet_name = forms.pet_name.data ,
                    phone_num = forms.phone_num.data, address = forms.address.data ,
                    mail = forms.mail.data, birthday = forms.birthday.data,
                    nick_name = forms.nick_name.data , Quote = forms.Quote.data,
                    Songs = forms.Songs.data,likes=forms.likes.data,hates=forms.hates.data,
                    what_us = forms.what_us.data,lastd = forms.lastd.data)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('slamform_layout.html' , forms=forms,owner=owner)


@jurzo.route('/slam/<slam_id>',methods=['GET','POST'])
@login_required
def slam(slam_id):

    slam=Page.query.get_or_404(slam_id)
    if current_user == slam.owner:
        return render_template('slam.html' , slam=slam)
    else:
        abort(403)


@jurzo.route('/slampdf/<slam_id>',methods=['GET','POST'])
def pdfslam(slam_id):
    slam=Page.query.get_or_404(slam_id)
    if current_user == slam.owner:
        slam_html = render_template('new_pdf.html',slam=slam)
        slam_pdf = pdfkit.from_string(slam_html,False)


        response = make_response(slam_pdf,False)

        response.headers['Content-Type']='application/pdf'
        response.headers['Content-Disposition']="inline; filename = out.pdf"
        return response



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@jurzo.com',
         recipients = [user.email])
    msg.body = '''To reset Your Password, visit the following link:
{}

    If you did not make the request , Please Ignore the email

    '''.format(url_for('reset_token',token=token,_external=True))
    mail.send(msg)


@jurzo.route("/reset_password",methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An link has been sent to your email to reset")
        return redirect(url_for('login'))
    return render_template('reset_request.html',form=form)


@jurzo.route("/reset_password/<token>",methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','Warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_pass
        db.session.commit()
        flash("Password has been updated {},You can now login.".format(user.username),category="success")
        return redirect(url_for('login'))

    return render_template('reset_token.html',form=form)














