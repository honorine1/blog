from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import Blog, User,Comment
from .forms import BlogForm, CommentForm, UpdateProfile
from flask.views import View,MethodView
from .. import db,photos
import markdown2



# Views
@main.route('/', methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    blogs = Blog.query.all()
    title = 'Home'
  
    return render_template('index.html',title = title, blogs=blogs)




@main.route('/blogs/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    # my_upvotes = Upvote.query.filter_by(pitch_id = Pitch.id)
    # userBlog = blog.query.filter_by(blog_id = Blog_id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        user_id = current_user
        # category = form.category.data
        print(current_user._get_current_object().id)
        new_blog = Blog(user_id =current_user._get_current_object().id, title = title,description=description)
      
        db.session.add(new_blog)
        db.session.commit()
          
        return redirect(url_for('main.index,profile/update.html'))
    # pitches=Pitch.query.filter_by(id = Pitch.id)
    return render_template('blogs.html',form=form)

# @main.route('/', methods = ['GET','POST'])
# def index():

#     '''
#     View root page function that returns the index page and its data
#     '''
#     blogs = Blog.query.filter_by(blog_id = Blog.id)
    
  
#     return render_template('index.html',title = title, blogs=blogs)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.index',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html')

@main.route('/comment/new/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    blogs=Blog.query.get(blog_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, blog_id = blog_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', blog_id= blog_id))

    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    return render_template('comments.html', form = form, comment = all_comments, blogs = blogs )



