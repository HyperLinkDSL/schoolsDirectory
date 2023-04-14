from django.db import models

from accounts.models import Profile
from schools.utils import counties


class School(models.Model):

    SCHOOL_TYPES = [
        ("PUBLIC", "Public"),
        ("PRIVATE", "Private"),
    ]

    name = models.CharField(max_length=500, blank=False)
    description = models.TextField(max_length=500, blank=False)
    address = models.TextField(max_length=500, blank=True)
    year_started = models.CharField(max_length=4, blank=True)
    primary_phone = models.CharField(max_length=25, blank=True)
    other_phone = models.CharField(max_length=25, blank=True)
    primary_email = models.CharField(max_length=100, blank=True)
    other_email = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    longitude = models.CharField(max_length=30, blank=False)
    latitude = models.CharField(max_length=30, blank=False)
    county = models.CharField(choices=counties(), blank=True, max_length=25)
    school_type = models.CharField(choices=SCHOOL_TYPES, blank=False, max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    is_approved = models.BooleanField(default=False)


class Gallery(models.Model):
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)


class Photo(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=1000, blank=False)
    photo = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)


