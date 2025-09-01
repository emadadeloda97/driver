import os
from flask import Flask, render_template, redirect, request, send_from_directory, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
import flask_login  

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'sandra'

db = SQLAlchemy(app)


LoginManager = LoginManager()
LoginManager.init_app(app)


@LoginManager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

#Database Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    def setHashPassword(pwd):
        return generate_password_hash(pwd)
    def checkPassword(self, pwd):
        return check_password_hash(self.password, pwd)

class registerForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    comPass = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    
class loginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


#Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = loginForm()
    if form.validate_on_submit():
        
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None:
            flash('Username does not exist', 'danger')
            
            return render_template('login.html', form=form)
        
        if not user.checkPassword(form.password.data):
            flash('Incorrect Password', 'danger')
            return render_template('login.html', form=form)
        flask_login.login_user(user)
        flash('Login Successful!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)
        

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        comPass = form.comPass.data
        if comPass != password:
            flash('Password does not match', 'danger')
            return render_template('register.html', form=form)
        hashPass = User.setHashPassword(password)
        db.session.add(User(username=username, password=hashPass))
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    folderPath = 'upload_'+flask_login.current_user.username if flask_login.current_user.is_authenticated else ''

    files = os.listdir(folderPath) if os.path.exists(folderPath) else []
    print(files)
    print(flask_login.current_user.username)
    return render_template('dashboard.html',files=files)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload():
    print(flask_login.current_user.username)
    if request.method == 'POST':
        
        
        files = request.files.getlist('files') # هنا الفرق
        print(files)
        if files is len(files) == 0:
            flash("No files selected for uploading.", "danger")
            return redirect(request.url)
        

        for file in files:

            folderName = 'upload_'+flask_login.current_user.username if flask_login.current_user.is_authenticated else ''
            filename = file.filename
            if not os.path.exists(folderName):  os.makedirs(folderName)
            filepath = os.path.join(folderName, filename)
            file.save(filepath)
            flash(f'File {filename} uploaded successfully.', 'success')
        return redirect(url_for('dashboard'))
        
      

        
        
        
        
        
        
        
        # file = request.files['file']
        # if file.filename == '':
        #     flash('No selected file', 'danger')
        #     return redirect(request.url)
        # folderPath = 'upload_'+flask_login.current_user.username if flask_login.current_user.is_authenticated else ''
        # if not os.path.exists(folderPath):os.makedirs(folderPath)
        # filepath = os.path.join(folderPath, file.filename)
        # file.save(filepath)
        # flash('File uploaded successfully', 'success')
        # print(file.filename)
    return render_template('upload.html')


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    folderPath = 'upload_'+flask_login.current_user.username if flask_login.current_user.is_authenticated else ''
    return send_from_directory(folderPath, filename)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    folderPath = 'upload_'+flask_login.current_user.username if flask_login.current_user.is_authenticated else ''
    filepath = os.path.join(folderPath, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"{filename} deleted successfully.", "success")
    else:
        flash("File not found.", "danger")
    return redirect(url_for("dashboard"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
