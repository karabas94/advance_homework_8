from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Comment

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'message')


class ContactFrom(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("Email can't be empty")
        return email

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if not subject:
            raise forms.ValidationError("Subject can't be empty")
        return subject

    def clean_message(self):
        message = self.cleaned_data['message']
        if not message:
            raise forms.ValidationError("Message can't be empty")
        return message
