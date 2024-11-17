from django.apps import AppConfig
from dotenv import load_dotenv

load_dotenv()


class PdfAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pdf_app'
