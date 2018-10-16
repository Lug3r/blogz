from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:solbadguy@localhost:8889/build-a-blog'                                                                                                                                                                                             
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, name, body):
        self.name = name
        self.body = body

    def is_valid(self):
        if self.name and self.body:
            return True
        else:
            return False


@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()

    return render_template('blogs.html', title="Build a Blog", 
        blogs=blogs)


@app.route('/blog', methods=['POST', 'GET'])
def blog():
     

    blog_id = request.args.get('id')

    if blog_id:
        blog = Blog.query.get(blog_id)

        return render_template('singpost.html', blog=blog)
    else:
        blogs = Blog.query.all()
        
        return render_template('blogs.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['newblog']
        new_blog = Blog(new_title, new_body)

        if new_blog.is_valid():
            db.session.add(new_blog)
            db.session.commit()

            return redirect('/blog?id=' + str(new_blog.id))

        else: 
            flash('you must include a title and name')
            return render_template('newpost.html', title='make a new post')


    else:
        return render_template('newpost.html', title='make a new post')



if __name__ == '__main__':
    app.run()