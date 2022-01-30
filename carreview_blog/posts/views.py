from flask import render_template, url_for,request,flash,Blueprint,redirect,abort
from flask_login import current_user, login_required
from carreview_blog import db, posts
from carreview_blog.models import BlogPost
from carreview_blog.posts.forms import BlogPostForm

posts= Blueprint('posts', __name__)

#createpost
@posts.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form= BlogPostForm()

    if form.validate_on_submit():

        blog_post= BlogPost(title=form.title.data,
                        text=form.text.data,
                        user_id= current_user.id
                        )
        db.session.add(blog_post)
        db.session.commit()
        flash('Post created')
        return redirect(url_for('core.home'))

    return render_template('create_post.html', form=form)

#postview
@posts.route('/<int:blog_post_id>/view')
def blog_post(blog_post_id):
    blog_post= BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)

#update post
@posts.route('/<int:blog_post_id>/update', methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post= BlogPost.query.get_or_404(blog_post_id)  

    if blog_post.author != current_user:
        abort(403)

    form=BlogPostForm()

    if form.validate_on_submit():

        blog_post.title=form.title.data
        blog_post.text=form.text.data
                                            
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('posts.blog_post', blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data= blog_post.title
        form.text.data= blog_post.text

    return render_template('create_post.html', title='Updating', form=form)

#delete
@posts.route('/<int:blog_post_id>/delete', methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Post Deleted')
    return redirect(url_for('core.home'))