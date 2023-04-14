from django import forms
from accounts.models import Profile


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

