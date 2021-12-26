from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from timeline.models import Post, Reply

class CreatePostForm(forms.Form):
    content = forms.CharField(label='', min_length=10, max_length=300)

class ReplyForm(forms.Form):
    content = forms.CharField(label='', min_length=1, max_length=100)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )