# crimeapp/forms.py

from django import forms
from .models import Members, Cases, Police
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class MemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['fname', 'lname', 'email', 'passwd', 'conform', 'age']

crimes = [('theft', 'Theft'), ('fraud', 'Fraud'), ('robbery', 'Robbery'), ('harrsing', 'Harrsing')]

class CaseForm(forms.ModelForm):
    typecrime = forms.ChoiceField(choices=crimes)
    class Meta:
        model = Cases
        fields = ['name', 'location', 'typecrime', 'Description']

class PoliceRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    police_id = forms.CharField(max_length=10)

    class Meta:
        model = Police
        fields = ['police_id', 'email', 'password1', 'password2']

class PoliceLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
