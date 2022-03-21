from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class AdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "firstname", "surname", "is_staff", "is_admin"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password != password_confirmation:
            self.add_error("password_confirmation", "Passwords didn't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.ser_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AdminUpdateForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["username", "email", "firstname", "surname", "is_staff", "is_admin"]

    def clean_password(self):
        return self.initial("passwords")

