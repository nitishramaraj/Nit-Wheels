
import email
from flask import render_template, request, Blueprint,redirect,url_for

from carreview_blog.models import BlogPost
from carreview_blog.posts.views import blog_post
import stripe

core= Blueprint('core', __name__)

@core.route('/')
def home():
    page= request.args.get('page', 1, type=int)
    blog_posts=BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)

    return render_template('home.html', blog_posts=blog_posts)

@core.route('/about')
def info():
    
    return render_template('info.html')

