import requests
from venv import create
from bs4 import BeautifulSoup
import traceback

from django.core.management import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from core.models import Faculty, Direction, Format, Document, Extractor



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--faculty', type=int, required=False)
        parser.add_argument('--direction', type=int, required=False)
        parser.add_argument('--format', type=int, required=False)

    def handle(self, *args, **options):
        documents = Document.objects.all()
        if options['format']:
            documents = documents.filter(format__id=options['format'])
        if options['direction']:
            documents = documents.filter(format__direction__id=options['direction'])
        if options['faculty']:
            documents = documents.filter(format__direction__faculty__id=options['faculty'])

        convert_pdf_to_txt('my1.pdf')


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text



def send_telegram_alert(text: str):
    LOG_TELEGTAM_CHAT_ID = '-679712895'
    TG_URL = "https://api.telegram.org/bot5321847235:AAH_2pcsNs9rReVKa2-SYxUYCgq23JAm08w/"
    method = TG_URL + "sendMessage"

    r = requests.post(method, data={
         "chat_id": LOG_TELEGTAM_CHAT_ID,
         "text": text
          })