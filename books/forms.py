from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Rating

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ("score", "comment")
        widgets = {
            "score": forms.Select(choices=[(i, f"{i} sao") for i in range(1, 6)], attrs={"class": "form-select"}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Nhận xét (tùy chọn)...", "class": "form-control"}),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
