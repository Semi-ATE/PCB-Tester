from django.shortcuts import render
import pcbtesterinterface.viewinterface as interface
from pcbtesterinterface.viewinterface import dec_permissionrequired

# Create your views here.
@dec_permissionrequired("admin")
def startup(request):
    errormessage = None
    if interface.ErroronStartup():
        errormessage = interface.getErrorMessageonStartup()
    if interface.ErroronStartup():
        statemessage = "Error on startup"
    else:
        statemessage = "Startup was successful"
    context = {
        'errormessage': errormessage,
        'startupstate': statemessage,
    }
    return render(request, 'startup_view/startup.html', context)




