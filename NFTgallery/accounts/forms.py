from django.core.exceptions import ValidationError
from django import forms

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
