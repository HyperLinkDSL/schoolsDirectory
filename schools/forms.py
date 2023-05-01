from django import forms
from schools.models import School, Photo


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
        self.fields['county'].widget.attrs.update({'class': 'form-control'})
        self.fields['school_type'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = School
        exclude = ['longitude', 'latitude', 'created', 'created_by', 'is_approved']

class ApproveSchoolForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['is_approved'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = School
        fields = ['is_approved']


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
        self.fields['county'].widget.attrs.update({'class': 'form-control'})
        self.fields['school_type'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = School
        exclude = ['created', 'created_by', 'is_approved', 'longitude', 'latitude']


class UploadPicturesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 2})

    class Meta:
        model = Photo
        exclude = ['created', 'created_by', 'is_active', 'school']
