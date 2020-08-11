# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from functools import wraps
from django.conf import settings

#-----------------------Init-----------------------#

def init(pluginmanager, condahandler, database):
    global pm
    global ch
    global databasemanager
    pm = pluginmanager
    ch = condahandler
    databasemanager = database
    databasemanager.init()
    
    
#-----------------------Init-----------------------#
#-----------------------React to view-----------------------#


def loadPlugin(pluginname):
    # load plugin with the help of pluginmanager
    return pm.addPlugin(pluginname)


def runPlugin():
    # get plugin with the help of pluginmanager and run it
    return pm.callPluginMethod()

def isPluginLoaded(pluginname):
    return pm.isPluginLoaded(pluginname)

def detectPlugin():
    # read eeprom
    return "plugin1"


def updatePlugins():
    # update plugin package with the help of condahandler
    ch.downloadPackage("Plugin1")


#-----------------------React to view-----------------------#
#-----------------------Change for different view-----------------------#


def checkPermission(permissionnamelist, response, *args, **kwargs):
    if('customuserid' in response.session and \
        databasemanager.containsUserid(response.session['customuserid']) and \
        databasemanager.hasPermission(response.session['customuserid'], permissionnamelist)):
        return True
    else:
        return False


def incorrectPermission(response, *args, **kwargs):
    if(settings.PERMISSION_INVALID_URL):    
        return redirect(settings.PERMISSION_INVALID_URL)
    else:
        raise Exception("The settigns file doesn't define \"PERMISSION_INVALID_URL\"")


def checkLogin(response, *args, **kwargs):
    if not 'customuserid' in response.session.keys():
        # invalid state
        raise Exception("Please select the CustomUserMiddleware middleware")
    if not databasemanager.containsDefaultUser:
        # invalid database
        raise Exception("Invalid Database")
    if not databasemanager.containsUserid(response.session['customuserid']):
        # invalid userid
        print("userid not defined in database")
        return False
    if databasemanager.getDefaultUser().id != response.session['customuserid']:
       return True
    else:
        return False


def incorrectUser(response, *args, **kwargs):
    if(settings.LOGIN_URL):    
        return redirect(settings.LOGIN_URL)
    else:
        raise Exception("The settigns file doesn't define \"LOGIN_URL\"")


#-----------------------Change for different view-----------------------#
#-----------------------Database-----------------------#


def containsDefaultUser():
    return databasemanager.containsDefaultUser()

def containsUserid(userid):
    return databasemanager.containsUserid(userid)

def containsUsername(username):
    return databasemanager.containsUsername(username)

def deleteUserByID(userid):
    return databasemanager.deleteUserByID(userid)

def getDefaultUser():
    return databasemanager.getDefaultUser()

def getSuperUser():
    return databasemanager.getSuperUser()

def getUserByID(userid):
    return databasemanager.getUserByID(userid)

def createsUser(username, psk, permissionnames):
    return databasemanager.createUser(username, psk, permissionnames)

def changePassword(userid, psk):
    return databasemanager.setPassword(userid, psk)

def isDefaultUser(userid):
    return databasemanager.isDefaultUser(userid)

def getAllAvailablePermissions():
    return databasemanager.permissionlist

def getAllUsers():
    return databasemanager.getAllUsers()

def authenticate(username, psk):
    if(containsUsername(username)):
        if getDefaultUser().username != username:
            user = databasemanager.getUserByName(username)
            if(databasemanager.matchpsk(user, username, psk)):
                return user
    return None
    


#-----------------------Database-----------------------#
#-----------------------Decorators-----------------------#


def dec_permissionrequired(*permissionnames):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if checkPermission(permissionnames, *args, **kwargs):
                return function(*args, **kwargs)
            else:
                return incorrectPermission(*args, **kwargs)
        return wrapper
    return decorator


def dec_loginrequired(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if checkLogin(*args, **kwargs):
            return function(*args, **kwargs)
        else:
            return incorrectUser(*args, **kwargs)
    return wrapper


#-----------------------Decorators-----------------------#