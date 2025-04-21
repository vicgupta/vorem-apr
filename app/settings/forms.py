from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class ProfileForm(FlaskForm):
    openai_api_key = StringField('OpenAI API Key', validators=[Optional()])
    gemini_api_key = StringField('Google Gemini API Key', validators=[Optional()])
    submit = SubmitField('Save Changes') 