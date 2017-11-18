import os
import shutil
import regex as re
from django.conf import settings
from django.core.management.base import BaseCommand

from bobross.models import Episode, Paints


class Command(BaseCommand):
    # args = '<foo bar ...>'
    help = 'Use this to populate the static files'

    def copy_cloud(self, epi_path, dirname, wordcloud_dir='bobross/media/wordclouds/'):
        try:
            project_root = settings.PROJECT_PATH
            full_path = os.path.join(project_root, 'bobross', 'static', 'media', 'wordclouds')
            cloud_path = os.path.join(epi_path, dirname+'.png')
            shutil.copy2(cloud_path, full_path)
        except FileNotFoundError:
            print("File not found")
        return 0

    def copy_transcript(self, epi_path, dirname, transcript_dir = 'bobross/media/transcripts/' ):
        static = settings.STATIC_URL
        project_root = settings.PROJECT_PATH
        full_path = os.path.join(project_root, 'bobross', 'static', 'media', 'transcripts')
        transcript_path = os.path.join(epi_path, dirname+'.txt')
        shutil.copy2(transcript_path, full_path)
        return 0

    def copy_painting(self, epi_path, dirname, painting_dir='/media/finished_paintings/'):
        static = settings.STATIC_URL
        project_root = settings.PROJECT_PATH
        full_path = os.path.join(project_root, 'bobross', 'static', 'media', 'finished_paintings')
        for root, dirs, files in os.walk(epi_path):
            for file in files:
                print(file)
                if file.startswith("painting"):
                    painting = file
        painting_path = os.path.join(epi_path, painting)
        shutil.copy2(painting_path, full_path)
        return 0

    def copy_resources(self):
        data_path = os.path.join(settings.PROJECT_PATH, 'bobross', 'data')
        for root, dirs, files in os.walk(data_path):
            # once inside of an epi directory, set episode fields
            for dirname in dirs:
                if dirname.startswith('Bob Ross -'):
                    epi_path = os.path.join(root, dirname)
                    self.copy_cloud(epi_path, dirname)
                    self.copy_transcript(epi_path, dirname)
                    self.copy_painting(epi_path, dirname)
        return 0

    def handle(self, *args, **options):
        #FIX create manytomany
        self.copy_resources()
        return 0