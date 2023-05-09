# Generated by Django 4.2 on 2023-05-02 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='school_photos/')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('thumbnail', models.ImageField(upload_to='thumbnails/')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schools.photo')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=500)),
                ('address', models.TextField(blank=True, help_text='Postal address', max_length=500)),
                ('year_started', models.CharField(blank=True, max_length=4)),
                ('primary_phone', models.CharField(blank=True, max_length=25)),
                ('other_phone', models.CharField(blank=True, max_length=25)),
                ('primary_email', models.CharField(blank=True, max_length=100)),
                ('other_email', models.CharField(blank=True, max_length=100)),
                ('website', models.CharField(blank=True, max_length=100)),
                ('longitude', models.CharField(max_length=30)),
                ('latitude', models.CharField(max_length=30)),
                ('county', models.CharField(blank=True, choices=[('01', 'Mombasa'), ('02', 'Kwale'), ('03', 'Kilifi'), ('04', 'Tana River'), ('05', 'Lamu'), ('06', 'Taita-Taveta'), ('07', 'Garissa'), ('08', 'Wajir'), ('09', 'Mandera'), ('10', 'Marsabit'), ('11', 'Isiolo'), ('12', 'Meru'), ('13', 'Tharaka-Nithi'), ('14', 'Embu'), ('15', 'Kitui'), ('16', 'Machakos'), ('17', 'Makueni'), ('18', 'Nyandarua'), ('19', 'Nyeri'), ('20', 'Kirinyaga'), ('21', "Murang'a"), ('22', 'Kiambu'), ('23', 'Turkana'), ('24', 'West Pokot'), ('25', 'Samburu'), ('26', 'Trans-Nzoia'), ('27', 'Uasin-Gishu'), ('29', 'Elgeyo-Marakwet'), ('30', 'Nandi'), ('31', 'Baringo'), ('32', 'Laikipia'), ('33', 'Nakuru'), ('34', 'Narok'), ('35', 'Kajiado'), ('36', 'Kericho'), ('37', 'Bomet'), ('38', 'Kakamega'), ('39', 'Bungoma'), ('40', 'Busia'), ('41', 'Siaya'), ('42', 'Kisumu'), ('43', 'Homa Bay'), ('44', 'Migori'), ('45', 'Kisii'), ('46', 'Nyamira'), ('47', 'Nairobi')], max_length=25)),
                ('school_type', models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
    ]
