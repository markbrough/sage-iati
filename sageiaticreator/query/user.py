from sageiaticreator.extensions import db
from sageiaticreator import models
import datetime, time

def user(user_id=None):
    if user_id:
        user = models.User.query.filter_by(id=user_id
                    ).first()
        return user
    else:
        users = models.User.query.all()
        return users

def user_by_username(username=None):
    if username:
        user = models.User.query.filter_by(username=username
                    ).first()
        return user
    return None

def updateUser(data):
    checkU = models.User.query.filter_by(username=data["username"]
                ).first()
    assert checkU
    checkU.username = data["username"]
    checkU.name = data["name"]
    checkU.email_address = data["email_address"]
    checkU.organisation = data["organisation"]
    db.session.add(checkU)
    db.session.commit()
    return checkU

def addUser(data):
    checkU = models.User.query.filter_by(username=data["username"]
                ).first()
    if not checkU:
        newU = models.User()
        newU.setup(
            username = data["username"],
            password = data.get('password'),
            name = data.get('name'),
            email_address = data.get('email_address'),
            organisation = data.get('organisation')
            )
        db.session.add(newU)
        db.session.commit()
        return newU
    return checkU

def addUserPermission(data):
    checkP = models.UserPermission.query.filter_by(
                user_id=data["user_id"],
                permission_name=data.get("permission_name"),
                organisation_slug=data["organisation_slug"],
                ).first()
    if not checkP:
        newP = models.UserPermission()
        newP.setup(
            user_id = data["user_id"],
            permission_name=data.get("permission_name"),
            organisation_slug=data["organisation_slug"],
            )
        db.session.add(newP)
        db.session.commit()
        return newP
    return None

def deleteUserPermission(permission_id):
    checkP = models.UserPermission.query.filter_by(id=permission_id).first()
    if checkP:
        db.session.delete(checkP)
        db.session.commit()
        return True
    return None

def deleteUser(username):
    checkU = models.User.query.filter_by(username=username).first()
    if checkU:
        db.session.delete(checkU)
        db.session.commit()
        return True
    return None

def userPermissions(user_id):
    checkP = models.UserPermission.query.filter_by(user_id=user_id
            ).all()
    return checkP
