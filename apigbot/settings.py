"""
Django settings for apigbot project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j)n3(7vb&vkg+rvpaknkr@$&hr+9b3lcu8jex6_$_#dw+p%i(c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
BASE_URL = "https://71e77d3d38cd.ngrok.io"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'line_interface',
    'closet',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'apigbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'apigbot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "apigbot",
        'HOST': "localhost",
        'PORT': "3306",
        'USER': "apigbot",
        'PASSWORD': "apigbot",
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    'work',
]

# LINE
LINE_CHANNEL_ACCESS_TOKEN = "AKF0OIbF+XpSlQdjj3bzOKmWPn7UIrV9ZfwY7gJmyLVDBhIapzbL8TFGaxaoo1uQPkTeB4i2eigpdDw47lpUuY4JZ9FvIzyT3ZH/ynYyRz2HjoJywdWILQlDFWXvhZcWkRQjfnC7tuP3SRQBttXxSQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "d9c80f3db916726032def3163150fd10"

INSTAGRAM_ID = "platinum_shops"
INSTAGRAM_DIR = "downloads"
INSTAGRAM_MAX_DOWNLOAD_INTERVAL = 10

WORK_DIR = "work"

WATERMARK_FONT_FILE = "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"
WATERMARK_FONT_SIZE = 40
WATERMARK_FONT_COLOR = (209, 25, 62)
WATERMARK_POINT = (0, 0)

CLOSET_FOOTER = "#APIGcloset #เสื้อผ้าสวย"
CLOSET_SUMMARY="""
APIG closet
จัดส่งสินค้า ทุกวัน จันทร์, พุธ, ศุกร์ ค่า โอนก่อนเที่ยงนะคะ

แจ้งสินค้า
1. [รหัสสินค้า][ชื่อสินค้า] สี [color]
    ราคา xxx บาท

2. [รหัสสินค้า][ชื่อสินค้า] สี [color]
    ราคา xxx บาท

ค่าส่ง 50 บาท
รวมยอด yyy บาท

💙กสิกรไทย 178-2-48702-5
นาย อภิรักษ์ โชคดีวนิชวัฒนา

- เก็บสินค้าหลังโอนแล้วเท่านั้น⚠
- รบกวนโอนภายใน1วันนะคะของหมดไวมาก
- ไม่รับเปลี่ยน/คืนทุกกรณี!!
(ยกเว้น ได้รับผิดแบบ/สี, size/ตำหนิ แจ้งเปลี่ยนภายใน2วันหลังเซ็นรับสินค้าและส่งกลับภายใน2-3วัน หากเกินกำหนดไม่รับเปลี่ยน)
- สั่งแล้วห้ามยกเลิก❌ กรณีสินค้าหมด 🚨เปลี่ยนแบบหรือคืนเงินเฉพาะตัวที่หมดเท่านั้น‼
( ห้ามยกเลิกตัวที่ได้ของนะคะ )

📌โอนแล้ว ส่งสลิปและแจ้งชื่อที่อยู่เบอร์โทรศัพท์ได้เลยน้าา
💓แจ้งเลขพัสดุทางแชท💓
"""
CLOSET_TRACKING="""
แจ้งเลขพัสดุนะคะ
สามารถเช็คสถานะได้ผ่าน
EMS 👉https://track.thailandpost.co.th
Kerry👉https://th.kerryexpress.com/th/track/
โดยกรอกรหัสพัสดุในช่องติดตามพัสดุ
*หากสถานะยังไม่ขึ้น ให้เช็คอีกครั้งตอนดึกๆค่ะ*

🚩กทม-ปริมณทล รอสินค้า1วัน
หรือ2วัน (กรณีสินค้าในคลังเยอะ)
🚩จังหวัดอื่นๆ ได้รับใน 2-3 วัน
(ทั้งนี้ไม่นับวันหยุด และวันที่ได้รับสินค้าอยู่ในช่วงวันที่กำหนด ขึ้นอยู่กับพื้นที่และจำนวนสินค้าในคลังค่ะ)

📌หากได้รับสินค้าผิดแบบ/size/สี/ตำหนิ แจ้งกลับภายใน2วันนับจากวันที่เซ็นรับสินค้าจากขนส่ง และส่งกลับภายใน2-3วัน หากเกินกำหนดงดเปลี่ยนทุกกรณีนะคะ

ขอบคุณที่อุดหนุนทางร้านมากๆค่าาา 🙏❤
"""

MAX_CAROUSEL_ACTION_OBJECT = 3
MAX_CAROUSEL_COLUMNS = 10
MAX_CAROUSEL_TITILE = 40
MAX_CAROUSEL_TEXT = 60
MAX_POSTBACK_LABEL = 20
