from werkzeug.utils import safe_join
from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory, abort, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a real secret key
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Directory to serve files from
FILES_DIRECTORY = "/Recordings"

# Mock database of users
users = {'user1': {'password': 'password1'}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('list_files'))
        else:
            return abort(401)  # Unauthorized
    else:
        return render_template("login.html", user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
@login_required
def list_files(req_path):
    # Joining the base and the requested path
    abs_path = safe_join(FILES_DIRECTORY, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_from_directory(FILES_DIRECTORY, req_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template_string("""
        <h1>Directory Listing</h1>
        <ul>
            {% for file in files %}
            <li><a href="{{ req_path|safe }}/{{ file|safe }}">{{ file }}</a></li>
            {% endfor %}
        </ul>
        <a href="/logout">Logout</a>
    """, files=files, req_path=req_path)

def signup():

    return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
