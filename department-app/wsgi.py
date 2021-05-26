from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "Secret Key"


# SqlAlchemy database configuration with MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:61353@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating a model table for my CRUD database
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50))
    name = db.Column(db.String(50))
    birthday = db.Column(db.Date)
    salary = db.Column(db.Integer)

    def __init__(self, department, name, birthday, salary):
        self.department = department
        self.name = name
        self.birthday = birthday
        self.salary = salary


# Route for querying on all employee data
@app.route('/')
def index():
    all_data = Employee.query.all()
    return render_template('index.html', employees=all_data)


# Route for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        department = request.form['department']
        name = request.form['name']
        birthday = request.form['birthday']
        salary = request.form['salary']
        my_data = Employee(department, name, birthday, salary)
        db.session.add(my_data)
        db.session.commit()
        flash('Employee Inserted Successfully')
        return redirect(url_for('index'))


# Route for updating an employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Employee.query.get(request.form.get('id'))
        my_data.department = request.form['department']
        my_data.name = request.form['name']
        my_data.birthday = request.form['birthday']
        my_data.salary = request.form['salary']
        db.session.commit()
        flash('Employee Updated Successfully')
        return redirect(url_for('index'))


# Route for deleting an employee
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Employee Deleted Successfully')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
