import os
from django.conf import settings
from datetime import datetime, timedelta
from tzlocal import get_localzone
from collections import defaultdict

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

from line_interface.models import LineUser
from .models import ClosetPost, ClosetImages

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


class ClosetHandler:

    def list(self, event, params):
        limit = settings.MAX_CAROUSEL_COLUMNS - 1
        offset = params['offset'] if 'offset' in params else 0
        limit = int(limit)
        offset = int(offset)

        carousel_columns = []
        for post in ClosetPost.objects.all().order_by('code')[offset:offset+limit]:
            description = post.description
            date_time = post.date.astimezone(
                get_localzone()).strftime("%H:%M:%S")
            for image in ClosetImages.objects.filter(code=post.code, thumbnail=True).order_by('-name')[:1]:
                action = PostbackAction(
                    label="ดูรายละเอียด",
                    data="action=view&code={}".format(post.code),
                )
                image_url = "{}{}?_={}".format(
                    settings.BASE_URL, image.src, datetime.now().timestamp())
                cc = CarouselColumn(
                    thumbnail_image_url=image_url,
                    title="{} {}".format(
                        post.code, date_time),
                    text=post.description[:settings.MAX_CAROUSEL_TEXT],
                    actions=[action],
                )
                carousel_columns.append(cc)
        if len(carousel_columns) == limit:
            cc = CarouselColumn(
                thumbnail_image_url=settings.BASE_URL,
                title="See more",
                text="ดูรายการต่อไป",
                actions=[
                    PostbackAction(
                        label="ดูรายการต่อไป",
                        data="action=list&offset={}".format(offset + limit),
                    ),
                ],
            )
            carousel_columns.append(cc)
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text',
            template=CarouselTemplate(columns=carousel_columns),
        )
        try:
            line_bot_api.reply_message(
                event.reply_token,
                template_message
            )
        except Exception as e:
            print(e)

    def view(self, event, params):
        code = params['code']
        messages = []
        closet_post = ClosetPost.objects.get(code=code)

        images = defaultdict(lambda: defaultdict(dict))
        for image in ClosetImages.objects.filter(code=code):
            itype = 'thumbnail' if image.thumbnail else 'original'
            images[image.name][itype] = settings.BASE_URL + image.src

        for name in images:
            messages.append(
                ImageSendMessage(
                    images[name]['original'],
                    images[name]['thumbnail']
                )
            )
        messages.append(TextSendMessage(text=closet_post.description))
        line_bot_api.reply_message(
            event.reply_token,
            messages
        )

    def download(self, event, params):
        code = params['code']
        name = params['name']

        image = ClosetImages.objects.get(code=code, name=name, thumbnail=False)
        thumbnail = ClosetImages.objects.get(
            code=code, name=name, thumbnail=True)

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                settings.BASE_URL + image.src,
                settings.BASE_URL + thumbnail.src
            )
        )

    def summary(self, event, params):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=settings.CLOSET_SUMMARY))

    def tracking(self, event, params):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=settings.CLOSET_TRACKING))

    def help(self, event):
        carousel_columns = []
        commands = {
            "list": "ดูรายการสินค้าวันนี้",
            "summary": "สรุปยอด (ฉบับร่าง)",
            "tracking": "แจ้งเลขพัสดุ",
        }
        for cmd in commands:
            description = commands[cmd]
            action = PostbackAction(
                label=cmd,
                data="action={}".format(cmd),
            )
            cc = CarouselColumn(
                title=cmd.capitalize(),
                text=description,
                actions=[action],
            )
            carousel_columns.append(cc)

        template_message = TemplateSendMessage(
            alt_text='Carousel alt text',
            template=CarouselTemplate(columns=carousel_columns),
        )
        line_bot_api.reply_message(
            event.reply_token,
            template_message
        )
