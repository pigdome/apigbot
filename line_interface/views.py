from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, StickerMessage, PostbackEvent
from linebot.exceptions import InvalidSignatureError, LineBotApiError

from .models import LineUser
from closet.handler import ClosetHandler

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
ch = ClosetHandler()

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    authen(event)
    try:
        fn = getattr(ch, event.message.text)
        fn(event)
    except Exception as e:
        print(e)
        ch.help(event)


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    authen(event)
    ch.help(event)

@handler.add(PostbackEvent)
def handle_postback(event):
    params = {}
    for data in event.postback.data.split("&"):
        k,v = data.split("=")
        params[k] = v
    
    action = params['action']
    try:
        fn = getattr(ch, action)
        fn(event, params)
    except Exception as e:
        print(e)
        print(action)
        print("WTF")
        ch.help(event)


def authen(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    line_id = event.source.user_id
    line_name = profile.display_name

    line_user_list = LineUser.objects.filter(line_id=line_id)

    if len(line_user_list) == 0:
        # create new user
        line_user = LineUser(line_id=line_id, line_name=line_name)
        line_user.save()