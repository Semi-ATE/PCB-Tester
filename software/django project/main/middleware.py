# -*- coding: utf-8 -*-
from main import viewinterface
def CustomUserMiddleware(get_response):
    
    def usermiddleware(request):
        # set user id to default user, if no userid is present
        if('customuserid' in request.session.keys() \
           and viewinterface.containsUserid(request.session['customuserid'])):
           # Do nothing
           pass
        elif (not 'customuserid' in request.session.keys()) and viewinterface.containsDefaultUser():
            # set userid in session dict
            request.session['customuserid'] = viewinterface.getDefaultUser().id
        elif 'customuserid' in request.session.keys() and \
            (not viewinterface.containsUserid(request.session['userid'])) and \
            viewinterface.containsDefaultUser():
            # invalid userid in session dict
            # username could be deleted
            request.session['customuserid'] = viewinterface.getDefaultUser().id
        elif not viewinterface.containsDefaultUser():
            # invalid Database
            raise Exception("Invalid Database")
        else:
            request.session['customuserid'] = viewinterface.getDefaultUser().id
        
        
        #set modified request object
        response = get_response(request)
        
        return response
    return usermiddleware