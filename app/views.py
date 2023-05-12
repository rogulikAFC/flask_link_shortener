import random
import string

from flask import render_template, redirect, url_for

from . import app, db

from .models import URLModel
from .forms import URLForm


def get_short():
    while True:
        short = ''.join(random.choices(string.ascii_letters + string.ascii_letters, k=6))

        if URLModel.query.filter(URLModel.short == short).first():
            continue

        return short
    

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()

    if form.validate_on_submit():
        url = URLModel()
        url.original_url = form.original_url.data
        url.short = get_short()
        db.session.add(url)
        db.session.commit()

        return redirect(url_for('urls'))

    return render_template('index.html', form=form, current='index')


@app.route('/urls', methods=['GET'])
def urls():
    urls = URLModel.query.all()
    return render_template('urls.html', current='news', urls=urls[::-1])


@app.route('/<string:short>', methods=['GET'])
def url_redirect(short):
    url = URLModel.query.filter(URLModel.short == short).first()

    if not url:
        return None
    
    url.visits += 1
    db.session.add(url)
    db.session.commit()

    return redirect(url.original_url)


if __name__ == '__main__':
    app.run(debug=True)
