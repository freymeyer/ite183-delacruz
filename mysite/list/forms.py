# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, MangaReadingList

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class MangaListUpdateForm(forms.ModelForm):
    class Meta:
        model = MangaReadingList
        fields = ['reading_status', 'num_chapters_read', 'num_volumes_read', 'user_rating']
        widgets = {
            'user_rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }