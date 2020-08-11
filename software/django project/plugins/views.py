from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST
from django.shortcuts import render
import main.viewinterface as interface
from main.viewinterface import dec_permissionrequired

@require_POST
@dec_permissionrequired("manageplugins")
def pluginsajax(request):
    if request.method == 'POST' and request.is_ajax():
        # TODO implement more logic -> state machine
        # TODO implement textarea in view
        requesttype = request.POST.get('type', None)
        pluginnameajax = request.POST.get('pluginname', None)
        message = "no message"
        result = "failure"
        
        # detect and load plugin
        if(requesttype == "detectloadplugin"):
            pluginname = interface.detectPlugin()
            if pluginname:
                if interface.loadPlugin(pluginname):
                    pluginnameajax = pluginname
                    message = "plugin detected and loaded: {}".format(pluginname)
                    result = "success"
                else:
                    message = "plugin detected, but not loaded. Try to update the plugins"
                    result = "failure"
            else:
                message = "no plugin detected. Instructions<- TODO in plugins/views.py"
                result = "failure"
        
        elif(requesttype == "update"):
            if(interface.updatePlugins()):
                message = "Plugins successfully updated."
                result = "success"
            else:
                message = "Plugins not updated."
                result = "failure"
        # run test
        elif(requesttype == "runtest"):
            if pluginnameajax:
                if interface.isPluginLoaded(pluginnameajax):
                    if(interface.runPlugin()):
                        message = "plugin finished"
                        result = "success"
                    else:
                        message = "plugin failed"
                        result = "failure"
                else:
                    message = "The plugin cannot be loaded. Please reload the plugin."
                    result = "failure"
            else:
                message = "Please detect and load the plugin"
                result = "failure"
        # return view
        ctx = {'message': message, 'status': result, 'pluginname': pluginnameajax}
        return HttpResponse(json.dumps(ctx), content_type='application/json')

@dec_permissionrequired("manageplugins")
def plugins(request):
    return render(request, 'plugins/plugins.html')