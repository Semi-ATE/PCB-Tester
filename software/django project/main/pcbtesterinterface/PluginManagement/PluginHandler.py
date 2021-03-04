# -*- coding: utf-8 -*-
import pluggy
import importlib
import pkgutil
import site


class PluginHandler(object):

    def __init__(self, pluginspecificationname, pluginspecification):
        self.pm = pluggy.PluginManager(pluginspecificationname)
        self.pm.add_hookspecs(pluginspecification)
    
    def importPackage(self, packagename):
        try:
            package = importlib.import_module(packagename)
        except:
            return False
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            modulename = "{}.{}".format(package.__name__,modname)
            if not ispkg and not self.isPluginLoaded(modulename):
                try:
                    plugin = importlib.import_module(modulename)
                    importlib.reload(plugin)
                    self.pm.register(plugin)
                except:
                    return False
        return True
    
    def loadAllPlugins(self, packagename):
        if self.importPackage(packagename):
            return True
        else:
            return False
    
    def getAll_Loaded_Pluginnames(self):
        return [name for name, plugin in self.pm.list_name_plugin()]
    
    def isPluginLoaded(self, pluginname):
        return pluginname in self.getAll_Loaded_Pluginnames()
    
    def reload(self, packagename):
        importlib.reload(site)
        self.removeAllPlugins()
        self.loadAllPlugins(packagename)
        return True
    
    def removeAllPlugins(self):
        for plugin in self.pm.get_plugins():
            self.pm.unregister(plugin)
        return True
    
    def runPlugin(self, name, printcallback):
        if name in self.getAll_Loaded_Pluginnames():
            plugin = self.pm.get_plugin(name)
            try:
                result = plugin.runPlugin(printcallback)
                return result
            except Exception as e:
                return False, "Unable to run plugin. Exception message: {}".format(str(e))
        else:
            return False, "Pluginname not found"

    def getHomePage(self, name):
        if name in self.getAll_Loaded_Pluginnames():
            plugin = self.pm.get_plugin(name)
            try:
                return plugin.getHomePage()
            except:
                return None
        else:
            return None