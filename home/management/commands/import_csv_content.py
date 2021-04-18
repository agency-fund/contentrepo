import csv
from django.core.management.base import BaseCommand, CommandError
from home.models import ContentPage, HomePage
from wagtail.core.rich_text import RichText


class Command(BaseCommand):
    help = 'Imports content via CSV'

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):
        def get_body(row):
            body = []
            row = row.splitlines()
            for line in row:
                if len(line) != 0:
                    body = body + [('paragraph', RichText(line))]
            return body

        path = options['path']
        home_page = HomePage.objects.first()
        with open(path, 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                contentpage = ContentPage(
                    title=row[0],
                    subtitle=row[1],
                    body=get_body(row[2]),
                    whatsapp_title=row[3],
                    whatsapp_subtitle=row[4],
                    whatsapp_body=get_body(row[5]),
                    messenger_title=row[6],
                    messenger_subtitle=row[7],
                    messenger_body=get_body(row[8]),
                    viber_title=row[9],
                    viber_subtitle=row[10],
                    viber_body=get_body(row[11]),
                    tags=row[12].split(" ")
                )
                home_page.add_child(instance=contentpage)
                contentpage.save_revision()

            self.stdout.write(self.style.SUCCESS('Successfully imported Content Pages'))
