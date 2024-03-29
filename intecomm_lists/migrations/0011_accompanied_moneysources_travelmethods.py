# Generated by Django 5.0.1 on 2024-02-22 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_lists", "0010_remove_arvdrugs_intecomm_li_name_b55bdc_idx_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Accompanied",
            fields=[
                (
                    "name",
                    models.CharField(
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "plural_name",
                    models.CharField(max_length=250, null=True, verbose_name="Plural name"),
                ),
                (
                    "display_name",
                    models.CharField(
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                ("extra_value", models.CharField(max_length=250, null=True)),
                ("version", models.CharField(default="1.0", editable=False, max_length=35)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "custom_name",
                    models.CharField(
                        blank=True,
                        help_text="A custom name/value to use on export instead of or in addition to `name`",
                        max_length=25,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Accompanied by",
                "verbose_name_plural": "Accompanied by",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "indexes": [
                    models.Index(
                        fields=["display_index", "display_name"],
                        name="intecomm_li_display_2b9504_idx",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="MoneySources",
            fields=[
                (
                    "name",
                    models.CharField(
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "plural_name",
                    models.CharField(max_length=250, null=True, verbose_name="Plural name"),
                ),
                (
                    "display_name",
                    models.CharField(
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                ("extra_value", models.CharField(max_length=250, null=True)),
                ("version", models.CharField(default="1.0", editable=False, max_length=35)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "custom_name",
                    models.CharField(
                        blank=True,
                        help_text="A custom name/value to use on export instead of or in addition to `name`",
                        max_length=25,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Money sources",
                "verbose_name_plural": "Money sources",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "indexes": [
                    models.Index(
                        fields=["display_index", "display_name"],
                        name="intecomm_li_display_504729_idx",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="TravelMethods",
            fields=[
                (
                    "name",
                    models.CharField(
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "plural_name",
                    models.CharField(max_length=250, null=True, verbose_name="Plural name"),
                ),
                (
                    "display_name",
                    models.CharField(
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                ("extra_value", models.CharField(max_length=250, null=True)),
                ("version", models.CharField(default="1.0", editable=False, max_length=35)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "custom_name",
                    models.CharField(
                        blank=True,
                        help_text="A custom name/value to use on export instead of or in addition to `name`",
                        max_length=25,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Travel methods",
                "verbose_name_plural": "Travel methods",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "indexes": [
                    models.Index(
                        fields=["display_index", "display_name"],
                        name="intecomm_li_display_e67514_idx",
                    )
                ],
            },
        ),
    ]
