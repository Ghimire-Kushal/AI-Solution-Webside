from django.contrib import admin
from .models import Service, Testimonial, BlogPost, GalleryImage, Event, ContactMessage, SiteSettings


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'project_name', 'is_active']
    list_filter = ['is_active', 'rating']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'published_at']
    list_filter = ['is_published', 'category']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'is_completed']
    list_filter = ['is_completed']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
