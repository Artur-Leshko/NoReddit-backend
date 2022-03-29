from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import UserProfile

User = get_user_model()

class AdminCreationForm(forms.ModelForm):
    '''
        Form for admin to create User
    '''
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        '''
            Meta class forAdminCreationForm
        '''
        model = User
        fields = ["username", "email", "is_staff", "is_admin"]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            self.add_error("password_confirmation", "Passwords didn't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

class AdminUpdateForm(forms.ModelForm):
    '''
        Form for admin to update User
    '''
    password = ReadOnlyPasswordHashField()

    class Meta:
        '''
            Meta class for AdminUpdateForm
        '''
        model = User
        fields = ["username", "email", "is_staff", "is_admin"]

    def clean_password(self):
        '''
            validating password
        '''
        return self.initial("password")


class AdminCreateProfileForm(forms.ModelForm):
    '''
        Form for admin to create UserProfile
    '''

    class Meta:
        '''
            Meta class for AdminUpdateUserProfileForm
        '''
        model = UserProfile
        fields = ['user', 'firstname', 'avatar', 'surname']

    def clean(self):
        cleaned_data = super().clean()

        user = cleaned_data.get("user")
        if UserProfile.objects.filter(user=user).exists():
            self.add_error('user', 'This user is already connected with some UserProfile')

        return cleaned_data


class AdminUpdateUserProfileForm(forms.ModelForm):
    '''
        Form for admin to update UserProfile
    '''
    user = forms.CharField(label='Related User model', disabled=True)

    class Meta:
        '''
            Meta class for AdminUpdateUserProfileForm
        '''
        model = UserProfile
        fields = ['user', 'firstname', 'avatar', 'surname']
