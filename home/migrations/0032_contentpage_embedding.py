# Generated by Django 4.1.9 on 2023-06-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_alter_contentpagerating_id_alter_contentpagetag_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentpage',
            name='embedding',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
