import os
from django.conf import settings
from datetime import datetime

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

    def list(selfm, event, params):
        name = params['name']

        carousel_columns = []
        for post in ClosetPost.objects.filter(date_frame=name).order_by('code'):
            if len(carousel_columns) == settings.MAX_CAROUSEL_COLUMNS:
                print("warn: MAX_CAROUSEL_COLUMNS")
                break

            description = post.description
            for image in ClosetImages.objects.filter(code=post.code, thumnail=True).order_by('-name')[:1]:
                action = PostbackAction(
                    label="ดูรายการ",
                    data="action=view&code={}".format(post.code),
                )
                image_url = "{}{}?_={}".format(
                    settings.BASE_URL, image.src, datetime.now().timestamp())
                cc = CarouselColumn(
                    thumbnail_image_url=image_url,
                    title="{} {}".format(
                        post.code, post.date.strftime("%H:%M:%S")),
                    text=post.description[:settings.MAX_CAROUSEL_TEXT],
                    actions=[action],
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

    def help(self, event):
        times = {
            "morning": "06.00-12.00",
            "afternoon": "12.00-18.00",
            "evening": "18.00 ขึ้นไป",
        }
        carousel_columns = []
        for time in times:
            description = times[time]
            action = PostbackAction(
                label="ดูรายการ",
                data="action=list&name={}".format(time),
            )
            cc = CarouselColumn(
                thumbnailImageUrl="",
                title=time.capitalize(),
                text="รายการในช่วง {}".format(description),
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
