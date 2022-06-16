from django.core.management.base import BaseCommand
import os
from pathlib import Path


class Command(BaseCommand):
    help = "Release the spiders"

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help="Name of the category")

    def handle(self, *args, **options):
        django_path = Path(__file__).resolve().parent.parent.parent.parent

        os.chdir(str(django_path) + "/scraper")
        os.system("scrapy crawl news -a category={}".format(options['category']))

