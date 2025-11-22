from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate   # ✅ migrations enabled

app = Flask(__name__)
app.secret_key = "supersecretkey"   # change this in production

# -------------------------
# Database setup
# -------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)   # ✅ enables flask db commands

# -------------------------
# User model
# -------------------------
class User(db.Model):
    __tablename__ = "users"   # explicit table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="Writer")   # NEW field
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
# -------------------------
# Routes
# -------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirmPassword']

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        # ✅ Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Logged in successfully!", "success")
            # ✅ Redirect to dashboard after login
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials, try again.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/forgot-password', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Password reset link sent to your email (demo).", "info")
        else:
            flash("Email not found.", "danger")
    return render_template('forgot-password.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        # Example: update name and email
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('orders.html')

@app.route('/submissions')
def submissions():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('submissions.html')

@app.route('/payouts')
def payouts():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('payouts.html')

@app.route('/messages')
def messages():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('messages.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# -------------------------
# Run the app
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
