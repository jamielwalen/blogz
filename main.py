from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Heaven123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    blog_title = db.Column(db.String(120))
    blog_entry = db.Column(db.String(500))

    def __init__(self, name, blog_title, blog_entry):
        self.name = name
        self.blog_title = blog_title
        self.blog_entry = blog_entry
        self.completed = False
        
@app.route('/')
def main():
    titles = Task.query.all()
    return render_template('todos.html',title="Build A Blog", 
        titles = titles)

#lost here. don't know how to get it to actually change pages once you click the link



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


if __name__ == '__main__':
    app.run()