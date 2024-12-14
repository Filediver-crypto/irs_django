from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    user_email = forms.EmailField(required=True)
    is_professor = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'user_email', 'is_professor', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Get count of existing users and add 1
        count = CustomUser.objects.count() + 1
        user.user_id = f'USER{count:03d}'  # This will create USER001, USER002, etc.
        user.user_email = self.cleaned_data['user_email']
        user.is_professor = self.cleaned_data['is_professor']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser 