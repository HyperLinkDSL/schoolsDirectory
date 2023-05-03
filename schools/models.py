import os

from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile
from schools.utils import counties


class School(models.Model):
    SCHOOL_TYPES = [
        ("PUBLIC", "Public"),
        ("PRIVATE", "Private"),
    ]

    name = models.CharField(max_length=500, blank=False)
    description = models.TextField(max_length=500, blank=False)
    address = models.TextField(max_length=500, blank=True, help_text="Postal address")
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

    def thumbnail(self):

        return Thumbnail.objects.filter(photo__school_id=self.pk).first()


# class Gallery(models.Model):
#     school = models.ForeignKey(School, on_delete=models.DO_NOTHING)
#     name = models.CharField(max_length=200, blank=False)
#     description = models.TextField(max_length=1000, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
#     is_active = models.BooleanField(default=False)


class Photo(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=f"school_photos/")
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)


class Thumbnail(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=f"thumbnails/")

    def __str__(self):
        return self.name


@receiver(post_save, sender=Photo)
def create_thumbnail(sender, instance, created, **kwargs):

    #  only generate thumbnail if there are no thumbnails for this photo
    if Thumbnail.objects.filter(photo=instance).exists():
        return

    if created:
        # Open the original photo
        original_photo = Image.open(instance.photo)

        # Create the thumbnail
        thumbnail_photo = original_photo.copy()
        thumbnail_photo.thumbnail((settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_HEIGHT))

        # Get the path to the photo file
        photo_path = instance.photo.path

        # Create the path to the thumbnail file
        thumbnail_dir = f"thumbnails/{instance.pk}"
        thumbnail_path = settings.MEDIA_ROOT + '/' + thumbnail_dir
        if not os.path.exists(thumbnail_path):
            os.makedirs(thumbnail_path)

        thumbnail_file = thumbnail_path + '/' + os.path.basename(photo_path)
        thumbnail_photo.save(thumbnail_file)

        # Create a new Thumbnail instance and save it
        thumbnail = Thumbnail(
            photo=instance,
            name=instance.name,
            thumbnail=thumbnail_dir + '/' + os.path.basename(photo_path)
        )
        thumbnail.save()
