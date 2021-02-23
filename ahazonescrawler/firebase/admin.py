import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

cred = credentials.Certificate(settings.getdict('FIREBASE_ADMIN_CREDENTIALS'))
firebase_admin.initialize_app(cred, settings.getdict('FIREBASE_ADMIN_OPTIONS'))

db_client = firestore.client()
storage_client = storage.bucket()

