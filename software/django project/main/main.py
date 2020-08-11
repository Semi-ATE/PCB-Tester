import pluggy

import main.PluginManagement.PluginHandler as pluginhandler
import main.CondaHandler as condahandler
import main.viewinterface as viewinterface
import main.Database.databasemanager as databasemanager



def run():
    '''
    Weist die jeweiligen Klassen einander zu
    Returns
    -------
    None.

    '''
    pm = pluggy.PluginManager("adapter")
    ph = pluginhandler.PluginHandler(pm, condahandler)
    viewinterface.init(ph, condahandler, databasemanager)
    
    
