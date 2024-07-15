from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet       #model to be used
        fields = ['text','photo'] #fields to be used


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email','password1','password2') #we are using built in froms's element/table
        

class TweetSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search')


