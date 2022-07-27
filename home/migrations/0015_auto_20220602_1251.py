# Generated by Django 3.2.7 on 2022-06-02 12:51

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models

import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_contentpage_is_whatsapp_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='is_whatsapp_template',
            field=models.BooleanField(default=False, verbose_name='Is Template'),
        ),
        migrations.AlterField(
            model_name='contentpage',
            name='whatsapp_body',
            field=wagtail.fields.StreamField([('Whatsapp_Message', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='document', required=False)), ('media', home.models.MediaBlock(icon='media', required=False)), ('message', wagtail.blocks.TextBlock(help_text='each message cannot exceed 4096 characters.', max_lenth=4096)), ('next_prompt', wagtail.blocks.CharBlock(help_text='prompt text for next message', max_length=20, required=False))], help_text='Each message will be sent with the text and media'))], blank=True, null=True),
        ),
    ]
