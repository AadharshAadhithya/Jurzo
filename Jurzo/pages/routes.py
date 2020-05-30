from Jurzo import db
from Jurzo.models import User, Page
from Jurzo.pages.fourms import PageForm
from flask import redirect, render_template, abort, make_response, url_for, Blueprint
from flask_login import login_required, current_user
import pdfkit

pages = Blueprint('pages', __name__)


@pages.route('/page/<username>', methods=['GET', 'POST'])
def page(username):
    owner = User.query.filter_by(username=username).first()
    forms = PageForm()
    if forms.validate_on_submit():
        page = Page(owner=owner, name=forms.name.data, pet_name=forms.pet_name.data,
                    phone_num=forms.phone_num.data, address=forms.address.data,
                    mail=forms.mail.data, birthday=forms.birthday.data,
                    nick_name=forms.nick_name.data, Quote=forms.Quote.data,
                    Songs=forms.Songs.data, likes=forms.likes.data, hates=forms.hates.data,
                    what_us=forms.what_us.data, lastd=forms.lastd.data)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('slamform_layout.html', forms=forms, owner=owner)


@pages.route('/slam/<slam_id>', methods=['GET', 'POST'])
@login_required
def slam(slam_id):

    slam = Page.query.get_or_404(slam_id)
    if current_user == slam.owner:
        return render_template('slam.html', slam=slam)
    else:
        abort(403)


@pages.route('/slampdf/<slam_id>', methods=['GET', 'POST'])
def pdfslam(slam_id):
    slam = Page.query.get_or_404(slam_id)
    if current_user == slam.owner:
        slam_html = render_template('new_pdf.html', slam=slam)
        slam_pdf = pdfkit.from_string(slam_html, False)

        response = make_response(slam_pdf, False)

        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "inline; filename = out.pdf"
        return response
