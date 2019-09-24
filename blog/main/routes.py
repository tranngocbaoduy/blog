from flask import request, render_template, Blueprint
from blog.models import Post

main = Blueprint('main', __name__)
 
@main.route("/")
@main.route("/home")
def home(): 
    page = request.args.get('page', 1, type=int) 
    posts = Post.objects.order_by('-date_posted').paginate(page=page, per_page=2)     
    return render_template('index.html',posts = posts, title='Home Page')
 
@main.route("/about")
def about():
    return render_template('about.html', title='About')

