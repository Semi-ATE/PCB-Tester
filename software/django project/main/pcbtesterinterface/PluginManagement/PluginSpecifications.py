import pluggy

hookspec = pluggy.HookspecMarker("semiate-deviceplugins")

"""
print callback can be called like
printcallback(content, timestamp = True)
printcallback(content, True)

the new line character has to be added manually
carriage return is supported
"""
@hookspec()
def runPlugin(printcallback):
    """return result of operation as bool and a message for the view"""
