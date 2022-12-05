# Generated by Django 4.1.3 on 2022-12-05 14:35

from django.db import migrations
import home.models
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0024_remove_sitesettings_content_variations_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contentpage",
            name="whatsapp_body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "Whatsapp_Message",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=False
                                    ),
                                ),
                                (
                                    "document",
                                    wagtail.documents.blocks.DocumentChooserBlock(
                                        icon="document", required=False
                                    ),
                                ),
                                (
                                    "media",
                                    home.models.MediaBlock(
                                        icon="media", required=False
                                    ),
                                ),
                                (
                                    "message",
                                    wagtail.blocks.TextBlock(
                                        help_text="each message cannot exceed 4096 characters.",
                                        max_lenth=4096,
                                    ),
                                ),
                                (
                                    "variation_messages",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "variation_restrictions",
                                                    wagtail.blocks.StreamBlock(
                                                        [
                                                            (
                                                                "gender",
                                                                wagtail.blocks.ChoiceBlock(
                                                                    choices=home.models.get_gender_choices
                                                                ),
                                                            ),
                                                            (
                                                                "health_literacy_level",
                                                                wagtail.blocks.ChoiceBlock(
                                                                    choices=home.models.get_health_lit_lvl_choices
                                                                ),
                                                            ),
                                                        ],
                                                        help_text="Restrict this variation to users with this profile value. Valid values must be added to the Site Settings",
                                                        max_num=1,
                                                        min_num=1,
                                                        required=False,
                                                        use_json_field=True,
                                                    ),
                                                ),
                                                (
                                                    "message",
                                                    wagtail.blocks.TextBlock(
                                                        help_text="each message cannot exceed 4096 characters.",
                                                        max_lenth=4096,
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                                (
                                    "next_prompt",
                                    wagtail.blocks.CharBlock(
                                        help_text="prompt text for next message",
                                        max_length=20,
                                        required=False,
                                    ),
                                ),
                            ],
                            help_text="Each message will be sent with the text and media",
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]
