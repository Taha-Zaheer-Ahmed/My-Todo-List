from flask import Flask, render_template
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
    date = db.Column(db.DateTime, default = datetime.now())

    def __repr__(self):
        return f" Sno: {self.sno} \n Title: {self.title}"

@app.route('/')
def hello_world():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()