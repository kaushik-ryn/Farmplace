from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# class UserRegisterForm(UserCreationForm):
#     role = forms.ChoiceField(
#         choices=User.ROLE_CHOICES,
#         widget=forms.Select(attrs={
#             'class': 'form-control',
#         }),
#         label="Register As"
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'role', 'password1', 'password2']

#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'placeholder': 'Choose a username',
#                 'class': 'form-control'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'placeholder': 'Enter your email address',
#                 'class': 'form-control'
#             }),
#         }

#         labels = {
#             'username': 'Username',
#             'email': 'Email Address',
#             'password1': 'Create Password',
#             'password2': 'Confirm Password',
#         }
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=(('farmer', 'Farmer'), ('consumer', 'Consumer'))
    )
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone', 'password1', 'password2']
