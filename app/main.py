from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from pyservicebinding import binding

sb = binding.ServiceBinding()
pg_list = sb.bindings("postgresql")
pg = pg_list[0]
username = pg["username"]
password = pg["password"]
database = pg["database"]
host = pg["host"]
port = pg["port"]

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://'+username+':'+password+'@'+host+':'+port+'/'+database
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class students(db.Model):
    __tablename__ = 'students'

    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

    def __repr__(self):
        return f"<Student {self.name}>"


@app.route('/')
def show_all():
    return render_template('show_all.html', students=students.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(name=request.form['name'], city=request.form['city'],
                               addr=request.form['addr'], pin=request.form['pin'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0')
