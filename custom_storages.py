# custom_storages.py
from django.conf import settings

print('saaying hello')

from storages.backends.s3boto3 import S3Boto3Storage

""""""
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    print('static storage ----------- saaying hello')


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
