# -*- coding: utf-8 -*-
from pcbtesterinterface.Database.permissions import permissionlist
from contextlib import contextmanager
import hashlib
import io
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import(
    create_engine,
    Column,
    String,
    Integer,
    Table,
    ForeignKey,
    Boolean,
    DateTime,
)




# superuser
superusername = "admin"
superuserstandardpsk = "admin"

# Default user
defaultuser = "defaultuser"
defaultuserpermission = "defaultuser"
defaultuserpsk = ""

# Base class
databasename = "test.sqlite"
engine = create_engine('sqlite:///'+databasename)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# Excel sheet name
sheetname = "plugindata"

#------------------------------------------------------- Declare models -------------------------------------------------------#
# User and Permissions
roles_users = Table(
    'roles_users',
    Base.metadata,
    Column('user_id', Integer(), ForeignKey('user.id')),
    Column('role_id', Integer(), ForeignKey('permission.id'))
)

# Permissions
class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)

# Users
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    psk = Column(String)
    permission = relationship(
        'Permission',
        secondary=roles_users,
        backref=backref('user', lazy='dynamic')
    )


    def __init__(self, username, psk, permission):
        self.username = username
        self.psk = psk
        self.permission = permission

    def __str__(self):
        return "id: {}, username: {}, psk: {}, permission: {}".format(self.id, self.username, self.psk, self.permission)



# plugins and plugincontainer
plugin_history = Table(
    'plugin_history',
    Base.metadata,
    Column('plugin_id', Integer(), ForeignKey('plugin.id')),
    Column('container_id', Integer(), ForeignKey('plugincontainer.id'))
)

# plugincontainer
class PluginContainer(Base):
    __tablename__ = 'plugincontainer'
    id = Column(Integer, primary_key=True)
    isScriptRunning = Column(Boolean())
    plugins = relationship(
        'Plugin',
        secondary=plugin_history,
        backref=backref('plugincontainer', lazy='dynamic')
    )

    def addPlugin(self, plugin):
        self.plugins.append(plugin)

    def __init__(self):
        self.isScriptRunning = False
        
    def __str__(self):
        return "id: {}, isScriptRunning: {}".format(self.id, self.isScriptRunning)

# Plugin
class Plugin(Base):
    __tablename__ = 'plugin'
    id = Column(Integer, primary_key=True)
    # plugin information
    packagename = Column(String)
    version = Column(String)
    scriptname = Column(String)
    # run information
    log = Column(String)
    resultstate = Column(Boolean)
    resultmessage = Column(String)
    # time information
    starttime = Column(DateTime)
    endtime = Column(DateTime)
    # user information
    username = Column(String)


    def __init__(self, starttime, endtime, username, packagename, version,
                 scriptname, resultstate, resultmessage, log=None):
        self.starttime = starttime
        self.endtime = endtime
        self.username = username
        self.packagename = packagename
        self.version = version
        self.scriptname = scriptname
        self.resultstate = resultstate
        self.resultmessage = resultmessage
        self.log = log
    
    def setLog(self, log):
        self.log = log

    def __str__(self):
        return "id: {}, packagename: {}, version: {}, scriptname: {}, log:{}"\
            .format(self.id, self.packagename, self.version, self.scriptname, self.log)

class _Plugin():

    def __init__(self, id, starttime, endtime, username, packagename, version,
                 scriptname, resultstate, resultmessage, log):
        self.id = id
        self.starttime = starttime
        self.endtime = endtime
        self.username = username
        self.packagename = packagename
        self.version = version
        self.scriptname = scriptname
        self.resultstate = resultstate
        self.resultmessage = resultmessage
        self.log = log

    def __str__(self):
        return "id: {}, packagename: {}, version: {}, scriptname: {}, log:{}"\
            .format(self.id, self.packagename, self.version, self.scriptname, self.log)

startup_versions = Table(
    'startup_versions',
    Base.metadata,
    Column('startup_id', Integer(), ForeignKey('startupcontainer.id')),
    Column('version_id', Integer(), ForeignKey('version.id'))
)

startup_pluginnames = Table(
    'startup_plugins',
    Base.metadata,
    Column('startup_id', Integer(), ForeignKey('startupcontainer.id')),
    Column('pluginname_id', Integer(), ForeignKey('pluginname.id'))
)

class Pluginname(Base):
    __tablename__ = 'pluginname'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name

class StartupContainer(Base):
    __tablename__ = 'startupcontainer'
    id = Column(Integer, primary_key=True)
    startupresult = Column(Boolean)
    startupmessage = Column(String)
    
    availableversions = relationship(
        "Version",
        secondary=startup_versions,
        backref=backref('startupcontainer', lazy='dynamic')
    )
    pluginlist = relationship(
        "Pluginname",
        secondary=startup_pluginnames,
        backref=backref('startupcontainer', lazy='dynamic')
    )
    currentversion = Column(String)
    packagename = Column(String)
    majorversion = Column(String)
    
    def __init__(self):
        self.startupresult = False
        self.startupmessage = "No Startup executed"
        self.currentversion = ""
        self.packagename = ""
        self.majorversion = ""

class Version(Base):
    __tablename__ = 'version'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
    
    

#------------------------------------------------------- Startup -------------------------------------------------------#
def startup():
    Base.metadata.create_all(engine)
    setPermissions()
    makeSuperUser()
    makeDefaultUser()
    makePluginContainer()
    makeStartupContainer()

def get_available_Pluginnames():
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            return [plugin.name for plugin in startupcontainer.pluginlist]
    return []

def set_available_Pluginnames(pluginnames):
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            startupcontainer.pluginlist = [Pluginname(name) for name in pluginnames]
            return True
    return False

def setStartupresult(state):
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            startupcontainer.startupresult = state
            return True
        else:
            return False

def getStartupresult():
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            return startupcontainer.startupresult

def setStartupMessage(message):
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            startupcontainer.startupmessage = message
            return True
        else:
            return False

def getStartupMessage():
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            return startupcontainer.startupmessage

def setAvailableVersions(versions):
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            startupcontainer.availableversions = [Version(version) for version in versions]
            return True
        else:
            return False

def getAvailableVersions():
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            return [version.name for version in startupcontainer.availableversions]

def setCurrentVersion(version):
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            startupcontainer.currentversion = version
            return True
        else:
            return False

def getCurrentVersion():
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            return startupcontainer.currentversion

def setPackageName(packagename):
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            startupcontainer.packagename = packagename
            return True
        else:
            return False

def getPackageName():
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            return startupcontainer.packagename

def setMajorVersion(majorversion):
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            startupcontainer.majorversion = majorversion
            return True
        else:
            return False

def getMajorVersion():
    with session_scope() as session:
        startupcontainer = session.query(StartupContainer).all()
        if(len(startupcontainer) == 1):
            startupcontainer = startupcontainer[0]
            return startupcontainer.majorversion



def isScriptRunning():
    with session_scope() as session:
        plugincontainer = session.query(PluginContainer).all()
        if(len(plugincontainer) == 1):
            plugincontainer = plugincontainer[0]
            return plugincontainer.isScriptRunning

def setScriptRunning(state):
    with session_scope() as session:
        plugincontainer = session.query(PluginContainer).all()
        if(len(plugincontainer) == 1):
            plugincontainer = plugincontainer[0]
            plugincontainer.isScriptRunning = state
            return True
        else:
            return False

def addPluginHistroy(starttime, endtime, username, pluginpackage, pluginversion,
                     pluginscriptname, log, resultstate, resultmessage):
    with session_scope() as session:
        plugincontainer = session.query(PluginContainer).all()
        if(len(plugincontainer) == 1):
            plugincontainer = plugincontainer[0]
            plugin = Plugin(starttime, endtime, username, pluginpackage, pluginversion,
                            pluginscriptname, resultstate, resultmessage, log)
            plugincontainer.addPlugin(plugin)
        else:
            return False

def getPluginHistory(session=None):
    if session:
        plugincontainer = session.query(PluginContainer).all()
        if(len(plugincontainer)==1):
            plugincontainer = plugincontainer[0]
            return plugincontainer.plugins
    else:
        with session_scope() as session:
            plugincontainer = session.query(PluginContainer).all()
            if(len(plugincontainer)==1):
                plugincontainer = plugincontainer[0]
                plugins = [_Plugin(plugin.id, plugin.starttime, plugin.endtime,
                           plugin.username, plugin.packagename, plugin.version,
                           plugin.scriptname, plugin.resultstate,
                           plugin.resultmessage, plugin.log)
                           for plugin in plugincontainer.plugins]
                return plugins


def setPermissions():
    with session_scope() as session:
        for permissionname in permissionlist:
            permission = session.query(Permission).filter_by(name=permissionname).all()
            if not permission:
                session.add(Permission(permissionname))

def makePluginContainer():
    with session_scope() as session:
        plugincontainer = session.query(PluginContainer).all()
        if(len(plugincontainer) == 0):
            session.add(PluginContainer())
        else:
            plugincontainer = plugincontainer[0]
            plugincontainer.isScriptRunning = False

def makeStartupContainer():
    with session_scope() as session:
        session.query(StartupContainer).delete()
        session.add(StartupContainer())

def makeDefaultUser():
    if not containsUsername(defaultuser):
        result = createUser(defaultuser, defaultuserpsk, defaultuserpermission)
        return result
    return False


def makeSuperUser():
    if not containsUsername(superusername):
        result = createUser(superusername, superuserstandardpsk, tuple(permissionlist))
        return result
    else:
        with session_scope() as session:
            user = getUserByName(superusername, session)
            userid = user.id
            currentpermissions = getUserpermissions(userid, session)
            permissionobjects = set(session.query(Permission).all())
            newpermissions = set(permissionlist) | set(currentpermissions)
            newpermissions = set(newpermissions) - (set(currentpermissions) - set(permissionlist))
            permissions = [permission for permission in permissionobjects \
                           for permissionname in newpermissions\
                           if permission.name == permissionname]
            user.permission = permissions
            return True


def hasPermission(userid, permissionnameslist):
    with session_scope() as session:
        if containsUserid(userid, session):
            user = getUserByID(userid, session)
            userpermissionlist = [permission.name for permission in user.permission]
            return set(permissionnameslist) <= set(userpermissionlist)
        return False


def existsPermission(permissionname, session=None):
    if not session:
        with session_scope() as session:
            return len(session.query(Permission).filter_by(name=permissionname).all()) > 0
    else:
        return len(session.query(Permission).filter_by(name=permissionname).all()) > 0

def getPermission(permissionname, session=None):
    if not session:
        with session_scope() as session:
            permissions = session.query(Permission).filter_by(name=permissionname).all()
            if(len(permissions) > 0):
                return permissions[0]
    else:
        permissions = session.query(Permission).filter_by(name=permissionname).all()
        if(len(permissions) > 0):
            return permissions[0]

def containsUsername(username, session=None):
    if not session:
        with session_scope() as session:
            return len(session.query(User).filter_by(username=username).all()) > 0
    else:
        return len(session.query(User).filter_by(username=username).all()) > 0

def containsDefaultUser(session=None):
    return containsUsername(defaultuser,session)

def containsSuperUser():
    return containsUsername(superusername)

def isDefaultUser(userid):
    with session_scope() as session:
        if(containsUserid(userid)):
            return getUserByID(userid, session).username==defaultuser
        return False

def createUser(username, psk, permissionnames):
    with session_scope() as session:
        if not containsUsername(username, session):
            if not isinstance(permissionnames, tuple):
                permissionnames = (permissionnames,)
            permissions = []
            for permissionname in permissionnames:
                if not existsPermission(permissionname, session):
                    return False
                else:
                    permissions.append(getPermission(permissionname, session))
            session.add(User(username,hashpsk(username,psk), permissions))
            return True
        return False

def setPassword(userid, psk):
    with session_scope() as session:
        if(containsUserid(userid)):
            user = getUserByID(userid, session)
            user.psk = hashpsk(user.username, psk)
            return True
        else:
            return False

def containsUserid(userid, session = None):
    if not session:
        with session_scope() as session:
            return len(session.query(User).filter_by(id=userid).all())>0
    else:
        return len(session.query(User).filter_by(id=userid).all())>0

def deleteUserByID(userid):
    with session_scope() as session:
        session.delete(getUserByID(userid))

def getDefaultUser(session=None):
    if(containsDefaultUser(session)):
        return getUserByName(defaultuser, session)
    else:
        return None

def getDefaultUsername():
    return defaultuser
    
def getSuperUser():
    if(containsSuperUser()):
        return getUserByName(superusername)
    else:
        return None

def getSuperUserid():
        return getUserID(superusername)

def getUserByName(username, session=None):
    if not session:
        with session_scope() as session:
            if containsUsername(username,session):
                return session.query(User).filter_by(username=username).all()[0]
    else:
        if containsUsername(username,session):
            return session.query(User).filter_by(username=username).all()[0]

def getUsername(userid):
    with session_scope() as session:
        if containsUserid(userid):
            return session.query(User).filter_by(id=userid).all()[0].username
        else:
            return None

def getUserID(username):
    with session_scope() as session:
        if containsUsername(username, session):
            return session.query(User).filter_by(username=username).all()[0].id
        else:
            return None

def getUserpermissions(userid, session=None):
    if not session:
        with session_scope() as session:
            if containsUserid(userid, session):
                permissions = getUserByID(userid, session).permission
                return [permission.name for permission in permissions]
    else:
        if containsUserid(userid, session):
            permissions = getUserByID(userid, session).permission
            return [permission.name for permission in permissions]

def getUserByID(id, session=None):
    if not session:
        with session_scope() as session:
            user = session.query(User).get(id)
            if(user):
                return user
    else:
        user = session.query(User).get(id)
        if(user):
            return user

def getAllUsers():
    with session_scope() as session:
        users = list(session.query(User).all())
        userlist = [(user.id, user.username, user.psk) for user in users]
        if(containsDefaultUser(session)):
            for user in userlist:
                if user[1] == getDefaultUsername():
                    userlist.remove(user)
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

def matchpsk(username, psk):
    with session_scope() as session:
        user = getUserByName(username, session)
        return(user.psk == hashpsk(username, psk))
def hashpsk(username, psk):
    m = hashlib.sha256()
    m.update((username+psk).encode('utf-8'))
    return m.hexdigest()

# session handling
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def writeExcelFile(df, sheetname):
    file_buffer = io.BytesIO()
    writer = pd.ExcelWriter(file_buffer, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheetname)
    worksheet = writer.sheets[sheetname]
    for idx, col in enumerate(df):
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
            ))
        worksheet.set_column(idx+1, idx+1, max_len)  # set column width
    writer.save()
    # reset pointer of stream
    file_buffer.seek(0)
    return file_buffer

def makeDataFrame():
    with session_scope() as session:
        plugins = getPluginHistory(session)
        data = {'pass': [], 'username': [], 'starttime': [], 'endtime': [],
                'packagename': [], 'version': [], 'scriptname': [],
                'resultmessage': [], 'log': []}
        if plugins:
            for plugin in plugins:
                data['starttime'].append(plugin.starttime)
                data['endtime'].append(plugin.endtime)
                data['username'].append(plugin.username)
                data['packagename'].append(plugin.packagename)
                data['version'].append(plugin.version)
                data['scriptname'].append(plugin.scriptname)
                data['log'].append(plugin.log)
                data['pass'].append(plugin.resultstate)
                data['resultmessage'].append(plugin.resultmessage)
        return pd.DataFrame(data)
        
def makePluginFileExcel():
    return writeExcelFile(makeDataFrame(), sheetname)

def makePluginFilePdf():
    # TODO
    return makePluginFileExcel(makeDataFrame(), sheetname)
