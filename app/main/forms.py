from flask_wtf import Form
from wtforms import StringField,BooleanField,SelectField,SubmitField,validators,TextAreaField
from wtforms.validators import DataRequired,Length,Email,Regexp
from ..models import Role,User
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
#表单类
class NameForm(Form):
    name=StringField("what is your name?",validators=[DataRequired()])
    submit=SubmitField("submit")


class EditProfileForm(Form):
    name = StringField('真实姓名',validators=[Length(0, 64)])
    location = StringField('地址',validators=[Length(0, 64)])
    about_me = TextAreaField('个人介绍')
    submit = SubmitField('提交')

class EditProfileAdminForm(Form):
    email=StringField('Email',validators=[DataRequired(), Length(1, 64),Email()])
    username = StringField('Username',validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    #上边正则表达式限制应户名的输入
    confirmed=BooleanField('Confirmed')
    role=SelectField('Role',coerce=int)
    name=StringField('Real name',validators=[Length(0, 64)])
    location=StringField('Location',validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]

        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

'''class PostForm(FlaskForm):
    body=TextAreaField("What's on your mind?",validators=[DataRequired()])
    submit=SubmitField('Submit')     这个是用来提交纯文本'''

class PostForm(Form):   #提交makedown文档
    body=PageDownField("What's on your mind?",validators=[DataRequired()])
    submit=SubmitField('Submit')


class CommentForm(Form):
    body = StringField('',validators=[DataRequired()])
    submit = SubmitField('submit')