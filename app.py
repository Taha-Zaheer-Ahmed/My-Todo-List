from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(1000),  nullable = False)
    date = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f" Sno: {self.sno} \n Title: {self.title}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('homepage.html', allTodo = allTodo)


@app.route('/edit/<int:sno>', methods=['GET', 'POST'])
def edit(sno):
    if request.method == "POST":
        todo = Todo.query.filter_by(sno=sno).first()
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

    
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit() 
        redirect('/')
    return redirect('/')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
