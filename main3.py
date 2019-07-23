from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'blah'


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Task', backref='owner')

    

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True,)
    completed = db.Column(db.Boolean)
    blog_title = db.Column(db.String(120))
    blog_entry = db.Column(db.String(500))
    
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, blog_title, blog_entry, completed, owner):
        self.blog_title = blog_title
        self.blog_entry = blog_entry
        self.completed = False
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        if 'username' not in session:
            redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect('/')

        else:
            pass
    return render_template('login.html')



@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def validate_info():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']

    username_error = ''
    password_error = ''
    verify_error = ''

    if username == '':
        username_error = 'Please enter a username'
        verify=''
        password=''

    elif len(username) < 3 or len(username) > 20:
            username_error = 'Please submit a username between 3 and 20 characters.'
            verify=''
            password=''

    else:
        for letter in username:
            if letter ==" ":
                username_error = 'Please use a valid character in your username. Spaces are not allowed.'
                verify=''
                password=''
        

    if password == '':
        password_error = 'Please enter a password'
        password=''
        verify=''

    elif len(password) < 3 or len(password) > 20:
            password_error = 'Please submit a password between 3 and 20 characters.'
            password=''
            verify=''

    else:
        for letter in password:
            if letter ==" ":
                password_error = 'Please use a valid character in your password. Spaces are not allowed.'
                password=''
                verify=''

    if verify == '':
        verify_error = 'Please enter a password to verify'
        verify=''
        password=''
    else:
        if password != verify:
            verify_error = 'Passwords do not match.'
            verify=''
            password=''
            

    if not username_error and not password_error and not verify_error:
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            session['username'] = username
            db.session.add(new_user)
            db.session.commit()
            return redirect('/new_post')
        else:
            return "<h1>Duplicate User</h1>"

    else:
        return render_template('register.html', username_error=username_error, password_error=password_error, verify_error=verify_error, username=username, password=password, verify=verify)
        
@app.route('/home')
@app.route('/')
def main():
        users = User.query.all()
        return render_template('home.html', users = users)


@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect('/login')
    else:
        del session['username']
        return redirect('/login')


@app.route('/all_posts', methods=['POST', 'GET'])
def index():
        num = request.args.get('id')

        if num == None:
            titles = Task.query.all()
            

            return render_template('todos.html',title="Build A Blog", 
            titles = titles)
        


@app.route('/blogs', methods=['POST', 'GET'])
def individual_post():
    num = request.args.get('id')
    num2 = Task.query.get(num)
    
    return render_template('individual.html', num2=num2, title="Build a Blog", titles= titles)

@app.route('/user', methods=['POST', 'GET'])
def user_posts():
    user_id = request.args.get('id') 
    blogs = Task.query.filter_by(owner_id = user_id)
    return render_template('user_blogs.html', blogs=blogs, title="Blogz")
    
@app.route('/blog', methods=['POST', 'GET'])
def users_posts():
    user_id = request.args.get('user') 
    blogs = Task.query.filter_by(owner_id = user_id)
    return render_template('user_blogs.html', blogs=blogs, title="Blogz")

    

@app.route('/new_post')
def new_post():
    if 'username' not in session:
        return redirect('/login')
    else:
        return render_template('todos2.html')



@app.route('/new_post', methods=['POST'])
def add_post():

    title_error=""
    entry_error=""
    

    task_name = request.form['blog_title']
    blog_title = request.form['blog_title']
    blog_entry = request.form['blog_entry']

    if blog_title == "":
        title_error = "Please submit a title."
        blog_entry = request.form['blog_entry']
    
    if blog_entry == "":
        entry_error = "Please submit an entry."
        blog_title = request.form['blog_title']
    
    if not title_error and not entry_error:
        titles = Task.query.all()
        owner = User.query.filter_by(username=session['username']).first()
        new_blog = Task(task_name, blog_title, blog_entry, owner)
        db.session.add(new_blog)
        db.session.commit()
        
        
    
        return redirect('/blogs?id={{titles.id}}')

    else:
        return render_template('todos2.html',title_error=title_error, entry_error=entry_error, blog_entry=blog_entry, blog_title=blog_title)


if __name__ == '__main__':
    app.run()