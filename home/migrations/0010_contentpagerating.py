# Generated by Django 3.2.7 on 2021-10-06 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('home', '0009_add_index_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentPageRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('helpful', models.BooleanField()),
                ('comment', models.TextField(blank=True, default='')),
                ('data', models.JSONField(blank=True, default=dict, null=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='home.contentpage')),
                ('revision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='wagtailcore.revision')),
            ],
        ),
    ]
