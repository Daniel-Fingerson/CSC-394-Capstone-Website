from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Intolerance, Diet, Profile


#Forms defined here can be natively rendered via Django's template tags
#Allows for user input that directly maps to Django models/any backend logic

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
    	model = User
    	fields = ["username", "email", "password1", "password2"]


class UserPref(forms.ModelForm):
    diet = forms.ModelChoiceField(queryset=Diet.objects.all(), initial=None, required=False)
    intolerances = forms.ModelMultipleChoiceField(queryset=Intolerance.objects.all(), required=False,widget=forms.CheckboxSelectMultiple)
 
    class Meta:
        model = Profile
        fields = [
             "diet","intolerances"
        ]