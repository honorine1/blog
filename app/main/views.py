from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from ..requests import getQuotes
from flask_login import login_required, current_user
from ..models import Blog, User,Comment
from .forms import BlogForm, CommentForm, UpdateProfile
from flask.views import View,MethodView
from .. import db,photos
import datetime
import markdown2



# Views
@main.route('/', methods = ['GET','POST'])
def index():
 

    '''
    View root page function that returns the index page and its data
    '''
    myDate= datetime.date.today()
   
    title = 'welcome to Blog web App'
    users = User.query.all()
    blogs = Blog.query.all()
    try:
       quotes = getQuotes()
    except Exception as e:
       quotes = "quotes unavailable"

  
    return render_template('index.html', myDate=myDate,title = title,users=users, blogs = blogs,quotes = quotes)




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
        flash('your blog has been created!','success') 
        return redirect(url_for('main.index'))
    # pitches=Pitch.query.filter_by(id = Pitch.id)
    return render_template('blogs.html',form=form)


@main.route("/delete/<int:id>",methods=["GET","POST"])
@login_required
def delete(id):
    deletedBlog = Blog.query.filter_by(id=id).first()
    db.session.delete(deletedBlog)
    db.session.commit()
    return redirect (url_for('main.index'))



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
    return render_template('index.html')

@main.route("/blog/<int:blog_id>/update", methods=['GET','POST'])
@login_required
def update_blog(blog_id):
    blog=Blog.query.get_or_404(blog_id)
    

    form =BlogForm()
    if form.validate_on_submit():
        blog.title=form.title.data
        blog.description=form.description.data
        db.session.commit()
        flash('your blog have been updated','success')
        return redirect(url_for('.index'))
    elif request.method == 'GET':
        form.title.data=blog.title
        form.description.data=blog.description
        
        
    return render_template('blogs.html',form=form)        
 



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



@main.route("/delete_comment/<int:comment_id>",methods=["GET","POST"])
@login_required
def delete_comment(comment_id):
    deleted_comment = Comment.query.filter_by(id=comment_id).first()
    db.session.delete(deleted_comment)
    db.session.commit()
    return redirect (url_for('main.index'))


  
# @main.route("/delete_comment/<int:id>",methods=["GET","POST"])
# @login_required
# def delete_comment(id):
#     deleted_comment = Comment.query.filter_by(id=id).first()
#     db.session.delete(deleted_comment)
#     db.session.commit()
#     return redirect (url_for('main.new_comment'))

# def search():
#     try:
#         con=pymysql.connect(user='root',password='  ',host='locolhost',database='db')
#         cur=con.cursor()
#         sql="select * from users where user_id='%s'"%user_id.get()
#         cur.execute(sql)

      
#         result=cur.fetchone()
#         username.set(result[1])


