# Generated by Django 3.2.5 on 2021-08-02 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0002_video_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
