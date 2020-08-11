# -*- coding: utf-8 -*-
#import CondaHandler
import importlib
import sys
import main.PluginManagement.PluginSpecifications as pluginspec

loadedplugins = {}


class PluginHandler(object):
    
    def __init__(self, pluggyobj, condahandler):
        pluggyobj.add_hookspecs(pluginspec.TestSpec())
        self.pm = pluggyobj
        self.condahandler = condahandler


    
    def addPlugin(self, name):
        importlib.reload(sys)
        try:
            if(name in loadedplugins.keys()):
                print("Already loaded")
                return True
            imported_module = importlib.import_module(name)
            print("loaded module "+name)
            plugin = imported_module.Plugin1()
            self.pm.register(plugin)
            loadedplugins[name] = plugin
            print("registered module "+name)
            return True
        except:
            print("unable to load module "+name)
            return False
    
    def isPluginLoaded(self, name):
        if name in loadedplugins.keys():
            return True
        else:
            return False    
        
    
    def removePlugin(self, name):
        try:
            if(name in loadedplugins.keys() and self.pm.is_registered(loadedplugins[name])):
                self.pm.unregister(loadedplugins[name])
                del loadedplugins[name]
                print("removed module "+name)
            else:
                print("Plugin not registered")
            return True
        except:
            print("unable to remove module "+name)
            return False
    
    def callPluginMethod(self):
        #CallPluginMethod
        result = self.pm.hook.testhook()
        #Compute results
        return result