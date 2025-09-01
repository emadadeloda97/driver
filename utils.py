from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User

def createUser(username, password,email):
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password,email = email)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def checkUser(username, password):
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        return True
    return False
