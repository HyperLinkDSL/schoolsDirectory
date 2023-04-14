from django import forms
from schools.models import School


class UpdateSchoolForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 2})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'rows': 2})
        self.fields['year_started'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['other_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['other_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['longitude'].widget.attrs.update({'class': 'form-control'})
        self.fields['latitude'].widget.attrs.update({'class': 'form-control'})
        self.fields['county'].widget.attrs.update({'class': 'form-control'})
        self.fields['school_type'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = School
        exclude = ['created', 'created_by', 'is_approved']


class CreateSchoolForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 2})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'rows': 2})
        self.fields['year_started'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['other_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['other_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['longitude'].widget.attrs.update({'class': 'form-control'})
        self.fields['latitude'].widget.attrs.update({'class': 'form-control'})
        self.fields['county'].widget.attrs.update({'class': 'form-control'})
        self.fields['school_type'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = School
        exclude = ['created', 'created_by', 'is_approved']
