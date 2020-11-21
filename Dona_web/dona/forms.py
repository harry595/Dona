from dona.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import help_board
from django_summernote.widgets import SummernoteWidget
from .models import Comment, messages

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)
    Nickname = forms.CharField(
        label='Enter Nickname', min_length=2, max_length=10)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_Nickname(self):
        Nickname = self.cleaned_data['Nickname'].lower()
        r = User.objects.filter(Nickname=Nickname)
        if r.count():
            raise ValidationError("Nickname already exists")
        return Nickname

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            Nickname=self.cleaned_data['Nickname']
        )
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = help_board
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('comment_text',)

class messagesForm(forms.ModelForm):
    class Meta:
        model=messages
        fields=('content',)
        