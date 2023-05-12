from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import URL, DataRequired


class URLForm(FlaskForm):
    original_url = StringField(
        'Вставьте ссылку',
        validators=[URL(message='Неверная ссылка'), DataRequired(message='Ссылка не может быть пустой')]
    )
    submit = SubmitField('Получить короткую ссылку')