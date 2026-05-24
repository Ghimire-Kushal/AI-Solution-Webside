from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('events/', views.events, name='events'),
    path('feedback/', views.feedback, name='feedback'),

    # Gemini AI chatbot API endpoint
    path('api/chat/', views.chat_api, name='chat_api'),
]
