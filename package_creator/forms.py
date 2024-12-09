from django import forms

class PackageForm(forms.Form):
    username = forms.CharField(max_length=100)
    passphrase = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
