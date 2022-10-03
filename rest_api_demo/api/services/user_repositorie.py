from database import db
from database.models import Users
class UsersRepositorie:
    """Users Model"""
    def __init__(self):
        return

    def createUser(username,email,password):
        
        user = Users(username,email,password)
        db.session.add(user)
        db.session.commit()

    def getUser(username):
        try:
            user = Users.query.filter_by(username = username).first()
            return {
                "id":user.id,
                "username":user.username,
                "password":user.password,
                "email":user.email
            }
        except:
            return 
    def getAllUsers():        
        try:            
            return Users.query.all()
        except:
            return 
    def updateUser(username,email,password):
        user = Users.query.filter_by(username = username).first()
        user.email = email
        user.password = password
        db.session.commit()

    def deleteUser(id):
        user = Users.query.filter_by(id = id).first()
        db.session.delete(user)
        db.session.commit()
