from django.core.management.base import BaseCommand, CommandError
from django.urls import URLResolver, URLPattern
from django.urls import get_resolver

class Command(BaseCommand):
    help = "Print all paths/endpoints"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        urls = self.get_urls_list()
        urls.sort()
        self.stdout.write(self.style.WARNING("The Endpoints are: "))
        for url in urls:
            self.stdout.write(self.style.SUCCESS(url))

    def get_urls_list(self):
        urls = [v for k,v in get_resolver().reverse_dict.items()]
        urls_list = [url[0][0][0] for url in urls]
        return list(set(urls_list))
