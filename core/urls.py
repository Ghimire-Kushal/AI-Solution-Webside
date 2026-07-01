from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
<<<<<<< HEAD
    path('our-services/', views.services_page, name='our_services'),
    path('portfolio/', views.services, name='services'),
=======
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
>>>>>>> e63a2c1 (fix bug)
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('feedback/', views.feedback, name='feedback'),
    path('gallery/', views.gallery, name='gallery'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),

    # Gemini AI chatbot API endpoint
    path('api/chat/', views.chat_api, name='chat_api'),
]
