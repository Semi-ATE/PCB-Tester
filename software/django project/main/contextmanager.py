from main import viewinterface


def usermanagement(request):
    if('customuserid' in request.session.keys()):
        if(viewinterface.containsUserid(request.session['customuserid'])):
            # user id in session dict and in database
            kwargs = {
                'customuser': viewinterface.getUserByID(request.session['customuserid']),
                'customuserpermissions': 
                    [permission.name for permission 
                      in viewinterface.getUserByID(request.session['customuserid']).permission],
                'customuseruserloggedin': (not viewinterface.isDefaultUser(request.session['customuserid']))
            }
            return kwargs
        else:
            # userid not in database, but in session dict
            # Failure in CustomUserMiddleware
            raise Exception("Invalid user selected in session dict")
    else:
        # user id not in session dict
        # CustomUserMiddleware not enabled
        raise Exception("Please enable CustomUserMiddleware")
