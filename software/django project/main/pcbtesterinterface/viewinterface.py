# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from functools import wraps
from django.conf import settings
from pcbtesterinterface import CondaHandler as ch
from pcbtesterinterface import epromhandler
import pcbtesterinterface.PluginManagement.PluginHandler as pluginhandler
import pcbtesterinterface.PluginManagement.PluginSpecifications as PluginSpecification
import pcbtesterinterface.Database.databasemanager as databasemanager

pm = pluginhandler.PluginHandler("semiate-deviceplugins",\
        PluginSpecification)

def startup():
    try:
        # read eprom
        epromresult, eprommessage = readeprom()
        if epromresult:
            installresult, installmessage = install_newest_package()
            if installresult:
                # startup successfull
                message = "New version successfully installed"
                databasemanager.setStartupresult(True)
                databasemanager.setStartupMessage(message)
                return True, message
            else:
                # error on startup
                databasemanager.setStartupresult(False)
                databasemanager.setStartupMessage(installmessage)
                return False, installmessage
        else:
            # error on startup
            databasemanager.setStartupresult(False)
            databasemanager.setStartupMessage(eprommessage)
            return False, eprommessage
    except Exception as e:
        # error on startup
        message = "An error occured during startup:\n"+str(e)
        databasemanager.setStartupresult(False)
        databasemanager.setStartupMessage(message)
        return False, message

def install_newest_package():
    # funktionsaufrufe für ch condahandler abändern
    detected_package = getDetectedPlugin()
    detected_major_version = getDetectedMajorVersion()
    if not detected_package or not detected_major_version:
        return False, "Invalid packagename: {} or invalid majorversion: {}"\
            .format(detected_package, detected_major_version)
    
    # download Package if necessary
    if not ch.isPackageInstalled(detected_package, detected_major_version):
        # download newest version
        success, resultmessage = ch.getNewestVersion(detected_package, detected_major_version)
        if not success:
            return False, resultmessage
        download_result, download_message = ch.downloadPackage(detected_package, resultmessage)
        if not download_result:
            return False, download_message
        downloadedpackage = True
    
    # get available versions
    success, result = ch.getAvailableVersions(detected_package, detected_major_version)
    if not result:
        return False, "No versions available"
    elif not success:
        return False, "Unable to search for available versions"
    
    setAvailableVersions(result)
    
    # update package if necessary
    if not downloadedpackage:
        success, result, message = ch.newVersion_available(detected_package, detected_major_version)
        if success and result:
            # install new version
            result, message = ch.install_newVersion(detected_package, detected_major_version)
            if not result:
                return False, message
        elif not success:
            return False, message
    
    # store available pluginnames in database
    updateAllDevicePluginNames()
    
    # get current version
    success, result, versionmessage = ch.getVersion_locally(detected_package)
    if success and result:
        setCurrentVersion(versionmessage)
    else:
        return False, versionmessage
    return True, "Successfully installed newest version"
    
    
#-----------------------Init-----------------------#
#-----------------------React to view-----------------------#

def loadAllDevicePlugins():
    # load plugin with the help of pluginmanager
    return pm.loadAllPlugins(getDetectedPlugin())

def readeprom():
    try:
        detected_packagename = epromhandler.getPackagename()
        detected_major_version = epromhandler.getMajorVersion()
        if detected_packagename and detected_major_version:
            databasemanager.setPackageName(detected_packagename)
            databasemanager.setMajorVersion(detected_major_version)
            return True, "The reading of the eprom was successful"
        else:
            return False, "The reading of the eprom was incorrect"
    except:
        return False, "An error occured while reading the eprom"

def downloadPackage(name, version=None):
    # detect plugin stored in the eeprom of the pcb
    return ch.downloadPackage(name, version)

def isPackageInstalled(name, version=None):
    return ch.isPackageInstalled(name, getDetectedMajorVersion(), version)

def install_newVersion(name):
    return ch.install_newVersion(name)

def runPlugin(name, printcallback):
    return pm.runPlugin(name, printcallback)

def getHomePage(name):
    return pm.getHomePage(name)

def reloadPLugins():
    return pm.reload(getDetectedPlugin())

def isPluginLoaded(pluginname):
    return pm.isPluginLoaded(pluginname)

def updatePlugin(name):
    reloadPLugins()
    return True

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
    if not databasemanager.containsDefaultUser():
        # invalid database
        raise Exception("Invalid Database")
    if not databasemanager.containsUserid(response.session['customuserid']):
        # invalid userid
        print("userid not defined in database")
        return False
    if getDefaultUserid() != response.session['customuserid']:
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
def getAllDevicePluginNames():
    return databasemanager.get_available_Pluginnames()

def updateAllDevicePluginNames():
    reloadPLugins()
    databasemanager.set_available_Pluginnames(pm.getAll_Loaded_Pluginnames())
    pm.removeAllPlugins()

def getDetectedPlugin():
    return databasemanager.getPackageName()

def getDetectedMajorVersion():
    return databasemanager.getMajorVersion()

def ErroronStartup():
    return not databasemanager.getStartupresult()

def getErrorMessageonStartup():
    return databasemanager.getStartupMessage()

def setAvailableVersions(versions):
    databasemanager.setAvailableVersions(versions)
    
def getAvailableVersions():
    return databasemanager.getAvailableVersions()

def setCurrentVersion(version):
    databasemanager.setCurrentVersion(version)

def getCurrentVersion():
    return databasemanager.getCurrentVersion()

def isScriptRunning():
    return databasemanager.isScriptRunning()

def setScriptRunning(state):
    return databasemanager.setScriptRunning(state)

def addTestResults(*args):
    """Description of args in databasemanager.addPLuginHistory"""
    return databasemanager.addPluginHistroy(*args)

def getPluginHistory():
    return databasemanager.getPluginHistory()

def containsDefaultUser():
    return databasemanager.containsDefaultUser()

def containsUserid(userid):
    return databasemanager.containsUserid(userid)

def containsUsername(username):
    return databasemanager.containsUsername(username)

def getUsername(userid):
    return databasemanager.getUsername(userid)

def getUserpermissions(userid):
    return databasemanager.getUserpermissions(userid)

def deleteUserByID(userid):
    return databasemanager.deleteUserByID(userid)

def getDefaultUser():
    return databasemanager.getDefaultUser()

def getDefaultUsername():
    return databasemanager.getDefaultUsername()

def getDefaultUserid():
    return databasemanager.getUserID(databasemanager.getDefaultUsername())

def getSuperUser():
    return databasemanager.getSuperUser()

def getSuperUserid():
    return databasemanager.getSuperUserid()

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

def getDefaultUserPermission():
    return databasemanager.defaultuserpermission

def getAllUsers():
    return databasemanager.getAllUsers()

def authenticate(username, psk):
    if(containsUsername(username)):
        if getDefaultUsername() != username:
            if(databasemanager.matchpsk(username, psk)):
                return databasemanager.getUserID(username)
    return False

def getPluginFileExcel():
    return databasemanager.makePluginFileExcel()

def getPluginFilePdf():
    return databasemanager.makePluginFilePdf()


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