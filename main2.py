from flask_sqlalchemy import SQLAlchemy

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

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


@app.route('/login')
@app.route('/')
def login():
    return render_template('login.html')

#@app.route('/login', methods=['POST'])
#def validate_username():

   


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def validate_info():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error =''

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

    counta = 0
    for letter in email:
        if letter == "@":
            counta = 1 + counta
    if counta > 1:
        email_error = "Please submit a valid email."

    countp = 0
    for letter in email:
        if letter == ".":
            countp = 1 + countp
    if countp > 1:
        email_error = "Please submit a valid email."
    
    if len(email) > 0:
        if len(email[:email.index('@')]) < 3 or len(email[:email.index('@')]) > 20:
                email_error = 'Put email with ONLY one . and ONE @'
    if len(email) == 0:
            email_error =''
            

    if not username_error and not password_error and not verify_error and not email_error:
        name = username
        return redirect('/home')
    else:
        return render_template('register.html', username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error, username=username, password=password, verify=verify, email=email)
        
@app.route('/home')
def main():
    titles = Task.query.all()
    return render_template('todos.html',title="Build A Blog", 
        titles = titles)





@app.route('/blog', methods=['POST', 'GET'])
def index():
    num = request.args.get('id')

    if num == None:
        titles = Task.query.all()
    
        return render_template('todos.html',title="Build A Blog", 
        titles = titles)
    else:
        num2 = Task.query.get(num)
    
        return render_template('individual.html', num2=num2, title="Build a Blog")
    

@app.route('/newpost')
def new_post():
    return render_template('todos2.html')



@app.route('/newpost', methods=['POST'])
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
        new_blog = Task(task_name, blog_title, blog_entry)
        db.session.add(new_blog)
        db.session.commit()

        
    
        return render_template('individual.html', num2=new_blog, title="Build a Blog")

    else:
        return render_template('todos2.html',title_error=title_error, entry_error=entry_error, blog_entry=blog_entry, blog_title=blog_title)