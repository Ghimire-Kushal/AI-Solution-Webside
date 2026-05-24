from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.panel_login, name='panel_login'),
    path('logout/', views.panel_logout_view, name='panel_logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='panel_dashboard'),

    # Services / Portfolio
    path('services/', views.services_list, name='panel_services'),
    path('services/add/', views.service_add, name='panel_service_add'),
    path('services/<int:pk>/edit/', views.service_edit, name='panel_service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='panel_service_delete'),

    # Blog
    path('blog/', views.blog_list, name='panel_blog'),
    path('blog/add/', views.blog_add, name='panel_blog_add'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='panel_blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='panel_blog_delete'),

    # Gallery
    path('gallery/', views.gallery_list, name='panel_gallery'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='panel_gallery_delete'),

    # Events
    path('events/', views.events_list, name='panel_events'),
    path('events/add/', views.event_add, name='panel_event_add'),
    path('events/<int:pk>/edit/', views.event_edit, name='panel_event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='panel_event_delete'),

    # Contact Messages
    path('contacts/', views.contacts_list, name='panel_contacts'),
    path('contacts/<int:pk>/', views.contact_detail, name='panel_contact_detail'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='panel_contact_delete'),

    # Testimonials
    path('testimonials/', views.testimonials_list, name='panel_testimonials'),
    path('testimonials/add/', views.testimonial_add, name='panel_testimonial_add'),
    path('testimonials/<int:pk>/edit/', views.testimonial_edit, name='panel_testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.testimonial_delete, name='panel_testimonial_delete'),

    # Site Settings & Password
    path('settings/', views.site_settings_view, name='panel_settings'),
    path('password/', views.change_password, name='panel_password'),
]
