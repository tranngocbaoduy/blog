from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])  
    picture = FileField('Add Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Post')

class CommentForm(FlaskForm): 
    content = TextAreaField('', validators=[DataRequired()])   
    submit = SubmitField('Send')
