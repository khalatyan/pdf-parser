import requests
from venv import create
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import traceback

from django.core.management import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from core.models import Faculty, Direction, Format, Document, DocumentType, Extractor

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
                try:
                    if doc[2].find('a'):
                        faculty, created = Faculty.objects.get_or_create(
                            title=doc[3].get_text()
                        )

                        direction, created = Direction.objects.get_or_create(
                            faculty=faculty,
                            title=doc[1].get_text()
                        )

                        format, created = Format.objects.get_or_create(
                            direction=direction,
                            title=doc[2].get_text(),
                            url=doc[2].find('a')['href']
                        )

                        if created:
                            get_document_urls(format)
                except:
                    send_telegram_alert(f"error site_parser \ndoc from table - {doc} \n{traceback.format_exc()}")


def get_document_urls(format):
    try:
        r = requests.get(f'{URL}{format.url}', verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')
        page_content = soup.find('div', class_='page_content')
        for doc_block in page_content.find_all('ul'):
            type_title = doc_block.find_previous().get_text()
            for doc in page_content.find_all('a'):
                type, created = DocumentType.objects.get_or_create(
                    title=type_title,
                )
                document, created = Document.objects.get_or_create(
                    format=format,
                    title=doc.get_text(),
                    type=type,
                    url=f'http://old.isu.ru/{doc["href"]}'
                )
    except:
        send_telegram_alert(f"error site_parser get_document_urls \nformat - {format} \n{traceback.format_exc()}")
        format.delete()


def send_telegram_alert(text: str):
    LOG_TELEGTAM_CHAT_ID = '-679712895'
    TG_URL = "https://api.telegram.org/bot5321847235:AAH_2pcsNs9rReVKa2-SYxUYCgq23JAm08w/"
    method = TG_URL + "sendMessage"

    r = requests.post(method, data={
        "chat_id": LOG_TELEGTAM_CHAT_ID,
        "text": text
    })