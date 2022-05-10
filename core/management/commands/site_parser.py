from venv import create
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from django.core.management import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from core.models import Faculty, Direction, Format, Document, Extractor

URL = 'http://old.isu.ru/ru/about/programs/'


class Command(BaseCommand):
    def handle(self, *args, **options):
        session = HTMLSession()
        r = session.get(f'{URL}list.html')
        r.html.render(sleep=10)
        soup = BeautifulSoup(r.html.raw_html, "html.parser")

        table_div = soup.find('div', id='table')
        for c in table_div.find_all('table'):
            table_doc = c
            extractor = Extractor(table_doc)
            extractor.parse()

            table_list = extractor.return_list()
            format_list = c.find_all('tr')
            for doc in table_list:
                if doc[2].find('a'):
                    faculty, created = Faculty.objects.get_or_create(
                        title=doc[3].get_text()
                    )

                    if created:
                        direction, created = Direction.objects.get_or_create(
                            faculty=faculty,
                            title=doc[1].get_text()
                        )

                    if created:
                        format, created = Format.objects.get_or_create(
                            direction=direction,
                            title=doc[2].get_text(),
                            url=doc[2].find('a')['href']
                        )

                    if created:
                        self.get_document_urls(format)

    
    def get_document_urls(self, format):
        session = HTMLSession()
        r = session.get(f'{URL}{format.url}')
        r.html.render()
        soup = BeautifulSoup(r.html.raw_html, "html.parser")
        page_content = soup.find('div', class_='page_content')
        for doc in page_content.find_all('a'):
            document, created = Document.objects.get_or_create(
                format=format,
                title=doc.get_text(),
                url=f'http://old.isu.ru/{doc["href"]}'
            )