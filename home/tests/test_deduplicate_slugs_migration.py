import importlib

from django.test import TestCase
from wagtail.models import Page

rename_duplicate_slugs = importlib.import_module(
    "home.migrations.0029_deduplicate_slugs"
).rename_duplicate_slugs


class DeduplicateSlugsMigrationTests(TestCase):
    def test_deduplictes_slugs(self):
        """
        Renames all pages with duplicate slugs, so that there are no two pages with the
        same slug.
        """
        home = Page.objects.first()
        duplicate = home.add_child(instance=Page(title="duplicate", slug="duplicate"))
        duplicate.add_child(instance=Page(title="duplicate", slug="duplicate"))
        home.add_child(instance=Page(title="unique", slug="unique"))

        rename_duplicate_slugs(Page)

        assert sorted(Page.objects.values_list("slug", flat=True)) == [
            "duplicate-1",
            "duplicate-2",
            "home",
            "root",
            "unique",
        ]
