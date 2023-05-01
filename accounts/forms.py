from django import forms
from accounts.models import Profile
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm


class UpdateProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['national_id'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'primary_phone', 'national_id', 'is_active', 'is_superuser']


class CreateProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['national_id'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'primary_phone', 'national_id']


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        # self.fields['primary_phone'].widget.attrs.update({'class': 'form-control'})
        # self.fields['national_id'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class RequestPasswordResetForm(forms.Form):

    email = forms.EmailField(max_length=150, required=True)

    def __init__(self, *args, **kwargs):
        super(RequestPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'


class ResetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Profile
        fields = ("new_password1", "new_password2")
