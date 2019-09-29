from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField,RadioField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError



class BlogForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	description = TextAreaField("Write your blog here",validators=[Required()])
	# category = RadioField('Label', choices=[ ('promotion','promotion'),('science','science'), ('interview','interview'),('technology','technology'),('product','product'),('artist','artist')],validators=[Required()])
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()
class UpdateProfile(FlaskForm):
	bio = TextAreaField('Tell us about you.',validators = [Required()])
	submit = SubmitField('Submit')
	

# class UpvoteForm(FlaskForm):
# 	submit = SubmitField()


# class Downvote(FlaskForm):
# 	submit = SubmitField()