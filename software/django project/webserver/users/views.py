from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, ChangePasswordForm
import pcbtesterinterface.viewinterface as interface
from pcbtesterinterface.viewinterface import dec_permissionrequired, dec_loginrequired

# TODO redundant code
@dec_permissionrequired("admin")
def register(request):
    if request.method == 'POST':
        permissionnames = set(interface.getAllAvailablePermissions())\
            -{interface.getDefaultUserPermission()}
        fields = {}
        for permissionname in permissionnames:
            fields[permissionname] = forms.BooleanField(required=False)
        formobj = type('DynamicUserRegisterForm', (UserRegisterForm,), fields)
        form = formobj(request.POST)
        if form.is_valid():
            # is valid?
            username = form.cleaned_data.get('username')
            if(interface.containsUsername(username)):
                # invalid username
                form.add_error('username', 'This username is already present')
                return render(request, 'users/register.html', {'form': form})
            # make user
            psk = form.cleaned_data.get('password1')
            permissions = []
            for permissionname in permissionnames:
                if form.cleaned_data.get(permissionname):
                    permissions.append(permissionname)
            permissions = set(permissions)|{interface.getDefaultUserPermission()}
            if(interface.createsUser(username, psk, tuple(permissions))):
                messages.success(request, f'Your account has been created\
                                 {username}! You are now able to log in')
                return redirect('login')
    else:
        permissionnames = set(interface.getAllAvailablePermissions())\
            -{interface.getDefaultUserPermission()}
        fields = {}
        for permissionname in permissionnames:
            fields[permissionname] = forms.BooleanField(required=False)
        formobj = type('DynamicUserRegisterForm', (UserRegisterForm,), fields)
        form = formobj()
    return render(request, 'users/register.html', {'form': form})




def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # is valid?
            userid = form.get_userid()
            request.session['customuserid'] = userid
            username = form.cleaned_data.get('username')
            messages.success(request, f'\
                             You are now logged in as {username}')
            if interface.ErroronStartup():
                messages.warning(request, "There was an error on startup")
            return redirect('about')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@dec_loginrequired
def profile(request):
    return render(request, 'users/profile.html')

@dec_permissionrequired('admin')
def userlist(request):
    if request.method == 'POST' and 'userid' in request.POST.keys():
        try:
            userid = int(request.POST['userid'])
            if('delete' in request.POST.keys() and request.POST['delete']=="True"):
                if (interface.getDefaultUserid() == userid or
                    interface.getSuperUserid() == userid):
                        messages.warning(request, "this user cannot be deleted")
                elif not interface.containsUserid(userid):
                    messages.error(request, "this userid isn't present", "danger")
                elif request.session['customuserid'] == userid:
                    messages.warning(request, "the current user cannot be deleted")
                else:
                    # delete user
                    interface.deleteUserByID(userid)
            elif('change' in request.POST.keys() and request.POST['change']=="True"):
                if (interface.getDefaultUserid() == userid):
                    messages.warning(request, "the password of this user cannot be changed")
                elif not interface.containsUserid(userid):
                    messages.error(request, "this userid isn't present", "danger")
                else:
                    # delete user
                    print("redirect to changepassword view")
                    request.session['changeuserid'] = userid
                    return redirect('changepassword')
        except:
            messages.error(request, "An error occured", "danger")
    return render(request, 'users/userlist.html', {'userlist': interface.getAllUsers()})

@dec_permissionrequired('admin')
def changepassword(request):
    if 'changeuserid' in request.session.keys():
        userid = request.session['changeuserid']
        if not userid or not isinstance(userid, int):
            messages.error(request, "Invalid userid", "danger")
        elif interface.getDefaultUserid() == userid:
            messages.warning(request, "the password of this user cannot be changed")
        elif not interface.containsUserid(userid):
            messages.error(request, "this userid isn't present", "danger")
        else:
            # redirect to change password view user
            form = ChangePasswordForm()
            context = {
                'form': form,
                'changeuserid': userid,
                'changeusername': interface.getUsername(userid)
            }
            del request.session['changeuserid']
            return render(request, 'users/changepassword.html', context)
        del request.session['changeuserid']
    elif(request.method == 'POST' and 'changeuserid' in request.POST.keys()):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            psk = form.cleaned_data.get('password2')
            # change psk for user
            if interface.changePassword(request.POST['changeuserid'], psk):
                messages.success(request, '\
                             Password changed successfully')
            else:
                messages.error(request, "password change failed", "danger")
            return redirect('userlist')
        context = {
            'form': form,
            'changeuserid': request.POST['changeuserid'],
            'changeusername': interface.getUsername(request.POST['changeuserid'])
        }
        return render(request, 'users/changepassword.html', context)
    return redirect('userlist')

def logout(request):
    request.session['customuserid'] = interface.getDefaultUserid()
    return render(request, 'users/logout.html', {})

def invalidpermissions(request):
    return render(request, 'users/invalidpermissions.html', {})
