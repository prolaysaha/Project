# Generated by Django 3.2.3 on 2021-05-16 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_videoseriessections_video_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoseriessections',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='series'),
        ),
    ]
