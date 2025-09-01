from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# create db object (no app yet)
db = SQLAlchemy()

# Example User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)


    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    


    

