from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String(100), nullable=False)

# Create all tables
db.create_all()

# Admin credentials
admin_email = 'admin@example.com'
admin_password = 'admin_password'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', message='Email already exists. Choose a different email.')

        # Create a new user
        new_user = User(name=name, email=email, password=password, birthday=birthday)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html', message='')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists and password matches
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return render_template('login.html', user_info=user)

        return render_template('login.html', message='Invalid email or password.')

    return render_template('login.html', message='')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        admin_email_input = request.form['admin_email']
        admin_password_input = request.form['admin_password']

        # Check admin credentials
        if admin_email_input == admin_email and admin_password_input == admin_password:
            users = User.query.all()
            return render_template('admin_dashboard.html', users=users)

        return render_template('admin_login.html', message='Invalid admin credentials.')

    return render_template('admin_login.html', message='')

if __name__ == '__main__':
    app.run(debug=True)
