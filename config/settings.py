from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

# ─── Installed Apps ───────────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

# ─── Middleware ───────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ─── Templates ────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'core.context_processors.unread_messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ─── Database ─────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─── Password Validators ──────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalisation ─────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

# ─── Static Files ─────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True

# ─── Sessions (cookie-based so Vercel read-only FS works) ─────
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# ─── CSRF & Trusted Origins ───────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# ─── Media Files ──────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Gemini API ───────────────────────────────────────────────
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')

# ─── OpenRouter API (Aria chatbot) ────────────────────────────
OPENROUTER_API_KEY = config('OPENROUTER_API_KEY', default='')

# ─── Login settings ───────────────────────────────────────────
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'

# ─── Jazzmin Admin Theme ──────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "AI-Solutions Admin",
    "site_header": "AI-Solutions",
    "site_brand": "AI-Solutions",
    "site_logo": "images/ai_solutions_logo.png",
    "login_logo": "images/ai_solutions_logo.png",
    "site_icon": None,
    "welcome_sign": "Welcome to AI-Solutions Admin",
    "copyright": "AI-Solutions © 2025",
    "search_model": [],
    "user_avatar": "images/ai_solutions_logo.png",
    "topmenu_links": [],
    "usermenu_links": [
        {"name": "Logout", "url": "/admin/do-logout/", "icon": "fas fa-sign-out-alt"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["auth"],
    "hide_models": ["auth.Group", "auth.User"],
    "custom_links": {
        "core": [
            {
                "name": "Users",
                "url": "/admin/auth/user/",
                "icon": "fas fa-user",
            },
            {
                "name": "Logout",
                "url": "/admin/do-logout/",
                "icon": "fas fa-sign-out-alt",
            },
        ]
    },
    "order_with_respect_to": [
        "core",
        "core.ServiceOffering",
        "core.PortfolioProject",
        "core.BlogPost",
        "core.GalleryImage",
        "core.Event",
        "core.Testimonial",
        "core.ContactMessage",
        "core.SiteSettings",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.ServiceOffering": "fas fa-cogs",
        "core.PortfolioProject": "fas fa-folder-open",
        "core.BlogPost": "fas fa-newspaper",
        "core.GalleryImage": "fas fa-images",
        "core.Event": "fas fa-calendar-alt",
        "core.Testimonial": "fas fa-star",
        "core.ContactMessage": "fas fa-envelope",
        "core.SiteSettings": "fas fa-cog",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": False,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-white",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": False,
}
