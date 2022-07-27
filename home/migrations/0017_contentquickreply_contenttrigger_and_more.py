# Generated by Django 4.0.6 on 2022-07-25 10:49

import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models

import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('home', '0016_auto_20220615_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentQuickReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'quick reply',
                'verbose_name_plural': 'quick replies',
            },
        ),
        migrations.CreateModel(
            name='ContentTrigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'content trigger',
                'verbose_name_plural': 'content triggers',
            },
        ),
        migrations.RemoveField(
            model_name='contentpage',
            name='messenger_quick_replies',
        ),
        migrations.RemoveField(
            model_name='contentpage',
            name='whatsapp_quick_replies',
        ),
        migrations.AlterField(
            model_name='contentpage',
            name='body',
            field=wagtail.fields.StreamField([('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='contentpage',
            name='messenger_body',
            field=wagtail.fields.StreamField([('messenger_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('message', wagtail.blocks.TextBlock(help_text='each message cannot exceed 2000 characters.', max_lenth=2000))], help_text='Each paragraph cannot extend over the messenger message limit of 2000 characters'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='contentpage',
            name='viber_body',
            field=wagtail.fields.StreamField([('viber_message', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('message', wagtail.blocks.TextBlock(help_text='each message cannot exceed 7000 characters.', max_lenth=7000))], help_text='Each paragraph cannot extend over the viber message limit of 7000 characters'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='contentpage',
            name='whatsapp_body',
            field=wagtail.fields.StreamField([('Whatsapp_Message', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='document', required=False)), ('media', home.models.MediaBlock(icon='media', required=False)), ('message', wagtail.blocks.TextBlock(help_text='each message cannot exceed 4096 characters.', max_lenth=4096)), ('next_prompt', wagtail.blocks.CharBlock(help_text='prompt text for next message', max_length=20, required=False))], help_text='Each message will be sent with the text and media'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='contentpagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag'),
        ),
        migrations.CreateModel(
            name='TriggeredContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='triggered_items', to='home.contentpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='triggered_content', to='home.contenttrigger')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuickReplyContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='quick_reply_items', to='home.contentpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quick_reply_content', to='home.contentquickreply')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contentpage',
            name='quick_replies',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='home.QuickReplyContent', to='home.ContentQuickReply', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='contentpage',
            name='triggers',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='home.TriggeredContent', to='home.ContentTrigger', verbose_name='Tags'),
        ),
    ]
