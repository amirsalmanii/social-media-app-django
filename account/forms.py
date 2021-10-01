from django import forms
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class EditProfile(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = Profile
        fields = ('bio', 'age')