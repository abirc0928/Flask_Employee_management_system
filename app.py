from flask import Flask, render_template, redirect, url_for, flash
from models import db, Employee , User 
from forms import EmployeeForm, SignupForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

#for data base setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

#for login setup
login_manager = LoginManager()
login_manager.init_app(app)  # Attach the LoginManager to the Flask app
login_manager.login_view = 'login'  # Set the login view route

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def homepage():
    employees = Employee.query.all()
    return render_template('index.html',employees=employees )

@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(
            name=form.name.data,
            phone=form.phone.data,
            salary=form.salary.data,
            designation=form.designation.data,
            short_description=form.short_description.data
        )
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('homepage'))  # Redirect to a homepage or list view
    
    return render_template('add_employee.html', form=form)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.phone = form.phone.data
        employee.designation = form.designation.data
        employee.salary = form.salary.data
        employee.short_description = form.short_description.data

        db.session.commit() 
        return redirect(url_for('homepage'))  # Redirect after successful updat
    return render_template('update_employee.html', employee=employee, form=form)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)  # Delete the contact
    db.session.commit()  # Commit the deletion to the database  
    return redirect(url_for('homepage'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            print('loging valid')
            return redirect(url_for('homepage'))
        
        flash('Login failed. Check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)