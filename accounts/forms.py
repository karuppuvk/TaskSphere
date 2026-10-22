# from django.contrib.auth.forms import UserCreationForm
# from .models import User


# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ("username", "email", "role")

from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter username",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Enter email address",
            }),
            "role": forms.Select(attrs={
                "class": "form-input",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = ""

        self.fields["password1"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Enter password",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Confirm password",
        })

        self.fields["email"].required = True
