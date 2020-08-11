from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, ChangePasswordForm
import main.viewinterface as interface
from main.viewinterface import dec_permissionrequired, dec_loginrequired

@dec_permissionrequired("admin")
def register(request):
    if request.method == 'POST':
        permissionnames = interface.getAllAvailablePermissions()
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
            if(interface.createsUser(username, psk, tuple(permissions))):
                messages.success(request, f'Your account has been created\
                                 {username}! You are now able to log in')
                return redirect('login')
    else:
        permissionnames = interface.getAllAvailablePermissions()
        print(permissionnames)
        fields = {}
        for permissionname in permissionnames:
            fields[permissionname] = forms.BooleanField(required=False)
        formobj = type('DynamicUserRegisterForm', (UserRegisterForm,), fields)
        form = formobj()
    return render(request, 'users/register.html', {'form': form})




def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        print("is form valid: {}".format(form.is_valid()))
        print(form.cleaned_data.get('username'))
        print(form.cleaned_data.get('password'))
        print("post")
        if form.is_valid():
            print("logged in")
            # is valid?
            user = form.get_user()
            request.session['customuserid'] = user.id
            username = form.cleaned_data.get('username')
            messages.success(request, f'\
                             You are now logged in as {username}')
            return redirect('about')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@dec_loginrequired
def profile(request):
    return render(request, 'users/profile.html', {})

@dec_permissionrequired('admin')
def userlist(request):
    if request.method == 'POST' and 'userid' in request.POST.keys():
        userid = int(request.POST['userid'])
        if('delete' in request.POST.keys() and request.POST['delete']=="True"):
            if (interface.getDefaultUser().id == userid or
                interface.getSuperUser().id == userid):
                    messages.warning(request, "this user cannot be deleted", 'danger')
            elif not interface.containsUserid(userid):
                messages.error(request, "this userid isn't present")
            else:
                # delete user
                interface.deleteUserByID(userid)
        elif('change' in request.POST.keys() and request.POST['change']=="True"):
            if (interface.getDefaultUser().id == userid):
                messages.warning(request, "the password of this user cannot be changed", 'danger')
            elif not interface.containsUserid(userid):
                messages.error(request, "this userid isn't present")
            else:
                # delete user
                print("return to changepassword view")
                request.session['changeuserid'] = userid
                return redirect('changepassword')
    return render(request, 'users/userlist.html', {'userlist': interface.getAllUsers()})

@dec_permissionrequired('admin')
def changepassword(request):
    if 'changeuserid' in request.session.keys():
        userid = request.session['changeuserid']
        if interface.getDefaultUser().id == userid:
            messages.warning(request, "the password of this user cannot be changed", 'danger')
        elif not interface.containsUserid(userid):
            messages.error(request, "this userid isn't present")
        else:
            # redirect to change password view user
            form = ChangePasswordForm()
            context = {
                'form': form,
                'changeuserid': userid,
                'changeusername': interface.getUserByID(userid).username
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
                messages.error(request, "password change failed")
            return redirect('userlist')
        context = {
            'form': form,
            'changeuserid': request.POST['changeuserid'],
            'changeusername': interface.getUserByID(request.POST['changeuserid']).username
        }
        return render(request, 'users/changepassword.html', context)
    return redirect('userlist')

def logout(request):
    request.session['customuserid'] = interface.getDefaultUser().id
    return render(request, 'users/logout.html', {})

def invalidpermissions(request):
    return render(request, 'users/invalidpermissions.html', {})
