from django import forms
from django.contrib.auth.forms import UsernameField
import pcbtesterinterface.viewinterface as interface
from django.contrib.auth import (
    password_validation,
)

username_max_length = 254


        

class UserCreationForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
    }
    username = UsernameField(
        label=("Username"),
    )
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password2', error)


class UserRegisterForm(UserCreationForm):
   
    class Meta:
        fields = ['username', 'password1', 'password2']






class UserLoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label= ("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct username and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.userid = None
        super().__init__(request, *args, **kwargs)

        # Set the max length and label for the "username" field.
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        if self.fields['username'].label is None:
            self.fields['username'].label = "Username"



    def authenticate(self, username, password):
        return interface.authenticate(username, password)


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            if(interface.getDefaultUsername() == username):
                raise self.get_invalid_login_error()
            self.userid = self.authenticate(username=username, password=password)
            if not self.userid:
                raise self.get_invalid_login_error()

        return self.cleaned_data

    def get_userid(self):
        return self.userid

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
        )




class UserPasswordChangeForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password2', error)


class ChangePasswordForm(UserPasswordChangeForm):
   
    class Meta:
        fields = ['password1', 'password2']
