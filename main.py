import datetime
import random
import string

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import URL, DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

db = SQLAlchemy(app)

class URLModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True, unique=True)
    original_url = db.Column(db.String(255), nullable=False)
    short = db.Column(db.String(255), nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())


with app.app_context():
    db.create_all()


class URLForm(FlaskForm):
    original_url = StringField(
        'Вставьте ссылку',
        validators=[URL(message='Неверная ссылка'), DataRequired(message='Ссылка не может быть пустой')]
    )
    submit = SubmitField('Получить короткую ссылку')

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
