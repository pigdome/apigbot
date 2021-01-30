from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import json
from datetime import datetime, timedelta
from itertools import dropwhile, takewhile

import instaloader

L = instaloader.Instaloader()


class Command(BaseCommand):
    help = "Collect post from instagram"

    def handle(self, *args, **options):
        posts = instaloader.Profile.from_username(
            L.context, settings.INSTAGRAM_ID).get_posts()

        YESTERDAY = datetime.now() - timedelta(1)
        YESTERDAY = YESTERDAY.date()
        TODAY = datetime.today().date()

        for post in takewhile(lambda p: p.date_utc.date() == TODAY, dropwhile(lambda p: p.date_utc.date() == YESTERDAY, posts)):
            L.download_post(post, settings.INSTAGRAM_DIR)
