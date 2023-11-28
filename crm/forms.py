from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

from django.forms import ModelForm #this is to use the models in our froms

from .models import Thought, Profile

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class ThoughtForm(ModelForm):

    class Meta:

        model = Thought
        fields = ['title','content','image','price','house_details']
        exclude = ['user',]

class UpdateUserForm(forms.ModelForm): #this form is to update the username and email id in the Profile Management

    password = None #we dont want to change the password

    class Meta:

        model = User
        
        fields = ['username', 'email']
        exclude = ['password1', 'password2',]


class UpdateProfileForm(forms.ModelForm):

    profile_pic = forms.ImageField(widget=forms.FileInput(attrs = {'class': 'from-control-file'})) 
    #data type -- Image Field , file input to make user uplaod the image, form control will be based upon our file

    class Meta:

        model = Profile
        
        fields = ['profile_pic',]

