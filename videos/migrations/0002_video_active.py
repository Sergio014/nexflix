# Generated by Django 4.1.3 on 2022-12-16 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
