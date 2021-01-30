from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from closet.models import ClosetImages, ClosetPost


class Command(BaseCommand):
    help = "Add watermark to images"

    def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        base36 = ''
        sign = ''

        if number < 0:
            sign = '-'
            number = -number

        if 0 <= number < len(alphabet):
            return sign + alphabet[number]

        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36

        return sign + base36
    
    def get_date(file):
        date = datetime.strptime(
            file[0:19], "%Y-%m-%d_%H-%M-%S")
        return date
        date = date + timedelta(hours=7)
        return date
    
    def get_date_frame(date):
        print(date, int(date.hour)+7)
        hour = int(date.hour) + 7
        if hour >= 0 and hour < 12:
            return "morning"
        elif hour >= 12 and hour < 18:
            return "afternoon"
        else:
            return "evening"

    def generate_code(file):
        timestamp = int(Command.get_date(file).timestamp())
        code = Command.base36encode(timestamp)
        code = "AP-{}".format(code)
        return code

    def handle(self, *args, **options):
        DOWNLOAD_DIR = settings.BASE_DIR / settings.INSTAGRAM_DIR
        WORK_DIR = settings.BASE_DIR / settings.WORK_DIR

        for file in os.listdir(DOWNLOAD_DIR):
            if file.endswith(".txt"):
                print(file)
                date = Command.get_date(file)
                date_frame = Command.get_date_frame(date)
                code = Command.generate_code(file)
                fh = open(DOWNLOAD_DIR / file, 'r')
                description = ""
                for line in fh.readlines():
                    text = None
                    if re.search(r"^([0-9]+)\.\-", line):
                        match = re.search(r"^([0-9]+)", line)
                        price = match.group(0)
                        text = "Price {}.-\n".format(price)
                    else:
                        text = re.sub(r"#[^\s]+", "", line)

                    description += text
                description += settings.POST_FOOTER
                ClosetPost.objects.update_or_create(
                    code=code, defaults={'description': description, 'date': date, 'date_frame': date_frame})

            elif file.endswith(".jpg"):
                code = Command.generate_code(file)
                number = re.sub(r"^.*_|\.jpg$", "", file)
                number = re.sub(r"UTC|_", "", number)
                if number == "":
                    number = "1"
                name = "{}-{}".format(code, number)
                img = Image.open(DOWNLOAD_DIR / file)
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(
                    settings.WATERMARK_FONT_FILE, settings.WATERMARK_FONT_SIZE)
                draw.text(settings.WATERMARK_POINT, code,
                          settings.WATERMARK_FONT_COLOR, font=font)
                img.save(WORK_DIR / file)

                ClosetImages.objects.update_or_create(
                    code=code, name=name, thumnail=False, defaults={'src': settings.STATIC_URL + file})
                
                # thumbnail
                file_thumbnail = re.sub(r"jpg$", "png", file)
                img.thumbnail((200, 302))
                img.save(WORK_DIR / file_thumbnail)
                
                ClosetImages.objects.update_or_create(
                    code=code, name=name, thumnail=True, defaults={'src': settings.STATIC_URL + file_thumbnail})
