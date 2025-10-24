# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'oLjCHNdmKBa5schL',
        'HOST': 'db.mqhmwffpbumevkhtdjnd.supabase.co',
        'PORT': '5432',
    }
}