from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
import re

def contains_required_chars(password):
    has_letter = bool(re.search(r'[a-zA-Z]', password))
    has_arithmetic = bool(re.search(r'[+\-*/]', password))
    return has_letter and has_arithmetic

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=40, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError('Old password is incorrect.')
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if self.user.password_restriction and not contains_required_chars(new_password):
            raise forms.ValidationError('New password must contain both letters and arithmetic symbols.')
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'New passwords do not match.')

        return cleaned_data

    
class AddUserForm(forms.Form):
    username = forms.CharField(max_length=40, required=True)

class CreateUserForm(forms.Form):
    login = forms.CharField(max_length=40, required=True, label='Login')
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Password')
    first_name = forms.CharField(max_length=50, required=False, label='First Name')
    last_name = forms.CharField(max_length=50, required=False, label='Last Name')
    role = forms.IntegerField(required=False, label='Role', initial=0)  # Default role is 0 (common user)
    is_blocked = forms.BooleanField(required=False, label='Is Blocked', initial=False)
    password_restriction = forms.BooleanField(required=False, label='Password Restriction', initial=False)

class AdminPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError('Old password is incorrect.')
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if self.user.password_restriction and contains_required_chars(new_password):
            raise forms.ValidationError('New password contains restricted characters.')
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'New passwords do not match.')

        return cleaned_data