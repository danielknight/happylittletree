import os
import shutil
import regex as re
from django.conf import settings
from django.core.management.base import BaseCommand

from bobross.models import Episode

class Command(BaseCommand):
    # args = '<foo bar ...>'
    help = 'Use this to update paint links for amzn to https'

    def update_clouds(self):
        E = Episode.objects.all()
        for e in E:
            cloud = e.wordcloud.name
            new_name = cloud.split(" ")
            new_name.remove("-")
            e.wordcloud.name = "-".join(new_name)
            e.save()

    def handle(self, *args, **options):
        self.update_clouds()
        # FIX create manytomany