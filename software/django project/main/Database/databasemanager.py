# -*- coding: utf-8 -*-
import main.Database.base as basemanager
from main.Database.permissions import permissionlist

import hashlib

superusername = "admin"
superuserstandardpsk = "admin"

defaultuser = "defaultuser"
defaultuserpsk = ""







def setPermissions(session):
    for permissionname in permissionlist:
        permission = session.query(Permission).filter_by(name=permissionname).all()
        if not permission:
            session.add(Permission(permissionname))
            # print("Created permission: {}".format(permissionname))
    session.commit()


def makeDefaultUser():
    if not containsUsername(defaultuser):
        result = createUser(defaultuser, defaultuserpsk, "defaultuser")
        # print("Default user created: {}".format(result))
        return result
    return False


def makeSuperUser():
    if not containsUsername(superusername):
        # print(tuple(permissionlist))
        result = createUser(superusername, superuserstandardpsk, tuple(permissionlist))
        # print("Super user created: {}".format(result))
        return result
    return False


def hasPermission(userid, permissionnameslist):
    if containsUserid(userid):
        user = getUserByID(userid)
        userpermissionlist = [permission.name for permission in user.permission]
        return set(permissionnameslist) <= set(userpermissionlist)
    return False


def existsPermission(permissionname):
    return len(session.query(Permission).filter_by(name=permissionname).all()) > 0

def getPermission(permissionname):
    permissions = session.query(Permission).filter_by(name=permissionname).all()
    if(len(permissions) > 0):
        return permissions[0]
    return None








def containsUsername(username):
    return len(session.query(User).filter_by(username=username).all()) > 0

def containsDefaultUser():
    return containsUsername(defaultuser)

def containsSuperUser():
    return containsUsername(superusername)

def isDefaultUser(userid):
    if(containsUserid(userid)):
        return getUserByID(userid).username==defaultuser
    return False


def createUser(username, psk, permissionnames):
    #try:
    if not containsUsername(username):
        if not isinstance(permissionnames, tuple):
            permissionnames = (permissionnames,)
        permissions = []
        for permissionname in permissionnames:
            if not existsPermission(permissionname):
                return False
            else:
                permissions.append(getPermission(permissionname))
        session.add(User(username,hashpsk(username,psk), permissions))
        session.commit()
        return True
    return False

def setPassword(userid, psk):
    if(containsUserid(userid)):
        user = getUserByID(userid)
        user.psk = hashpsk(user.username, psk)
        session.commit()
        return True
    else:
        return False

def containsUserid(userid):
    try:
        return session.query(User).get(userid)!=None
    except Exception:
        return None


def deleteUserByID(userid):
    session.delete(getUserByID(userid))
    session.commit()


def getDefaultUser():
    if(containsDefaultUser()):
        return getUserByName(defaultuser)
    else:
        return None


def getSuperUser():
    if(containsSuperUser()):
        return getUserByName(superusername)
    else:
        return None

def getUserByName(username):
    if containsUsername(username):
        return session.query(User).filter_by(username=username).all()[0]
    else:
        return None


def getUserByID(id):
    user = session.query(User).get(id)
    if(user):
        return user
    else:
        return None


def getAllUsers():
    userlist = list(session.query(User).all())
    if(containsDefaultUser()):
        userlist.remove(getDefaultUser())
    return userlist


def updateUser(user, newusername=None, newpassword=None, newpermissions=None):
    if user:
        if(newusername):
            user.username = newusername
        if(newpassword):
            user.psk = newpassword
        if(newpermissions):
            user.permissions = newpermissions
        return True
    return False


def matchpsk(user, username, psk):
    return(user.psk == hashpsk(username, psk))


def hashpsk(username, psk):
    # TODO
    print("Username: "+username)
    print("Password: "+psk)
    m = hashlib.sha256()
    m.update((username+psk).encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()





def init():
    basemanager.init()
    global session
    global User
    global Permission
    from main.Database.base import session
    from main.Database.User import User
    from main.Database.Permission import Permission
    basemanager.makeMetaData()
    setPermissions(session)
    makeSuperUser()
    makeDefaultUser()