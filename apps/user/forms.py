from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import *
from django.contrib.auth.validators import UnicodeUsernameValidator


# registering user
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# authenticating user
class LoginForm(AuthenticationForm):
    username = CharField(widget=TextInput())
    password = CharField(widget=PasswordInput())


class UpdateUserForm(ModelForm):
    username = CharField(
        max_length=150,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
        validators=[UnicodeUsernameValidator()],
    )
    first_name = CharField(
        max_length=150,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    last_name = CharField(
        max_length=150,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    email = EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
