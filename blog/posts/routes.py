from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from blog.models import Post,Comment,User
from blog.posts.forms import (PostForm,CommentForm) 
from datetime import datetime
from flask_login import current_user, login_required 
from blog.posts.utils import save_post_picture

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():  
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title= form.title.data, content=form.content.data, author= current_user.id)
        if form.picture.data: 
            picture_file = save_post_picture(form.picture.data)
            post.image_file = picture_file
        flash(f'Your post have been created', 'success')
        post.save()
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='New Post', 
                                    form = form, legend='New Post')


@posts.route("/delete_comment/<comment_id>", methods=['GET', 'POST']) 
def delete_comment(comment_id):
    print(comment_id) 
    comment = Comment.objects.get_or_404(id=comment_id)
    post_id = comment.post.id
    comment.delete()
    flash(f'You have been deleted a comment', 'success')
    return redirect(url_for('posts.post',post_id=post_id))

@posts.route("/post/<post_id>", methods=['GET', 'POST'])
def post(post_id):   
    post = Post.objects.get_or_404(id=post_id)    
    form = CommentForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        content = form.content.data 
        user = User.objects.get_or_404(email=current_user.email)  
        comment = Comment(post=post,author=user,content=content)
        comment.save() 
    form.content.data = ""
    comments = Comment.objects(post=post)    
    return render_template('post.html', title='Post',
                                    post = post,comments = comments,form=form)

@posts.route("/post/<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):   
    post = Post.objects.get_or_404(id=post_id) 
    if post.author.email != current_user.email:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data 
        post.save()
        flash(f'You have been updated a post', 'success') 
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    image_file = url_for('static', filename='post_pics/' + post.image_file)
    return render_template('new_post.html', title='Update Post', 
                            image_file=image_file, form=form, legend='Update Post') 

@posts.route("/post/<post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):   
    post = Post.objects.get_or_404(id=post_id) 
    if post.author.email != current_user.email:
        abort(403) 
    post.delete()
    flash(f'You have been deleted a post', 'success')
    return redirect(url_for('main.home'))
