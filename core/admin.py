import json
from datetime import timedelta, date

from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path
from django.utils import timezone
from django.utils.html import format_html

from .models import (
    Service, ServiceOffering, PortfolioProject,
    Testimonial, BlogPost, GalleryImage,
    Event, ContactMessage, SiteSettings,
)


# ─── Inline helpers ──────────────────────────────────────────────────────────

def image_preview(obj, field='image', width=60):
    img = getattr(obj, field, None)
    if img:
        return format_html('<img src="{}" width="{}" style="border-radius:6px;object-fit:cover;">', img.url, width)
    return '—'


# ─── Shared base for service admin classes ────────────────────────────────────

class ServiceAdminBase(admin.ModelAdmin):
    list_display_links = ['title']
    list_filter = []
    list_editable = ['is_featured', 'order']
    search_fields = ['title', 'description', 'client_name']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']

    @admin.display(description='')
    def thumb(self, obj):
        return image_preview(obj, 'image', 50)


# ─── Service Offerings ────────────────────────────────────────────────────────

@admin.register(ServiceOffering)
class ServiceOfferingAdmin(ServiceAdminBase):
    list_display = ['thumb', 'title', 'category', 'is_featured', 'order']
    fieldsets = (
        ('Service Info', {
            'fields': ('title', 'slug', 'category', 'icon', 'is_featured', 'order'),
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'features'),
        }),
        ('Media', {
            'fields': ('image',),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(record_type=Service.TYPE_SERVICE)

    def save_model(self, request, obj, form, change):
        obj.record_type = Service.TYPE_SERVICE
        super().save_model(request, obj, form, change)


# ─── Portfolio Projects ───────────────────────────────────────────────────────

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(ServiceAdminBase):
    list_display = ['thumb', 'title', 'category', 'client_name', 'is_featured', 'order']
    fieldsets = (
        ('Project Info', {
            'fields': ('title', 'slug', 'category', 'icon', 'is_featured', 'order'),
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'features'),
        }),
        ('Client & Media', {
            'fields': ('client_name', 'image'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(record_type=Service.TYPE_PORTFOLIO)

    def save_model(self, request, obj, form, change):
        obj.record_type = Service.TYPE_PORTFOLIO
        super().save_model(request, obj, form, change)


# ─── Testimonial ─────────────────────────────────────────────────────────────

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'name', 'company', 'rating_stars', 'project_name', 'is_active', 'created_at']
    list_display_links = ['name']
    list_filter = []
    list_editable = ['is_active']
    search_fields = ['name', 'company', 'content', 'project_name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Reviewer', {'fields': ('name', 'role', 'company', 'photo')}),
        ('Review', {'fields': ('rating', 'project_name', 'content', 'is_active')}),
        ('Meta', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    @admin.display(description='')
    def thumb(self, obj):
        return image_preview(obj, 'photo', 40)

    @admin.display(description='Rating')
    def rating_stars(self, obj):
        full = int(obj.rating)
        stars = '★' * full + '☆' * (5 - full)
        return format_html('<span style="color:#FBB040;">{}</span> <small>{}</small>', stars, obj.rating)


# ─── BlogPost ────────────────────────────────────────────────────────────────

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'title', 'author', 'category', 'is_published', 'published_at']
    list_display_links = ['title']
    list_filter = []
    list_editable = ['is_published']
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Post', {'fields': ('title', 'slug', 'author', 'category', 'image')}),
        ('Content', {'fields': ('excerpt', 'content')}),
        ('Publishing', {'fields': ('is_published', 'published_at')}),
        ('Meta', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='')
    def thumb(self, obj):
        return image_preview(obj, 'image', 50)


# ─── GalleryImage ────────────────────────────────────────────────────────────

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'title', 'description', 'uploaded_at']
    list_display_links = ['title']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at', 'image_preview_large']
    fieldsets = (
        (None, {'fields': ('title', 'description', 'image', 'image_preview_large', 'uploaded_at')}),
    )

    @admin.display(description='')
    def thumb(self, obj):
        return image_preview(obj, 'image', 60)

    @admin.display(description='Preview')
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:480px;max-height:320px;border-radius:10px;object-fit:contain;">',
                obj.image.url,
            )
        return '—'


# ─── Event ───────────────────────────────────────────────────────────────────

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'title', 'date', 'location', 'status_badge']
    list_display_links = ['title']
    list_filter = []
    list_editable = []
    search_fields = ['title', 'description', 'location']
    fieldsets = (
        ('Event Details', {'fields': ('title', 'description', 'date', 'location', 'image')}),
        ('Status', {'fields': ('is_completed',)}),
    )

    @admin.display(description='')
    def thumb(self, obj):
        return image_preview(obj, 'image', 50)

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_completed:
            return format_html('<span style="background:#374151;color:#9ca3af;padding:2px 10px;border-radius:20px;font-size:.75rem;">Completed</span>')
        return format_html('<span style="background:#065f46;color:#34d399;padding:2px 10px;border-radius:20px;font-size:.75rem;">Upcoming</span>')


# ─── ContactMessage ──────────────────────────────────────────────────────────

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'country', 'job_title', 'read_badge', 'created_at']
    list_filter = []
    search_fields = ['name', 'email', 'company', 'country', 'job_title', 'job_details']
    readonly_fields = ['name', 'email', 'phone', 'company', 'country', 'job_title', 'job_details', 'created_at']
    actions = ['mark_as_read']
    fieldsets = (
        ('Contact Info', {'fields': ('name', 'email', 'phone')}),
        ('Company & Role', {'fields': ('company', 'country', 'job_title')}),
        ('Job Details', {'fields': ('job_details',)}),
        ('Status', {'fields': ('is_read', 'created_at')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

    @admin.display(description='Status')
    def read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color:#6b7280;font-size:.78rem;">Read</span>')
        return format_html('<span style="background:#1d4ed8;color:#93c5fd;padding:2px 8px;border-radius:20px;font-size:.75rem;font-weight:600;">New</span>')

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')


# ─── SiteSettings ────────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Branding', {'fields': ('site_name', 'tagline', 'logo')}),
        ('Contact', {'fields': ('email', 'phone', 'address', 'time_zone')}),
        ('Social Links', {'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'github_url')}),
    )
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


# ─── Custom Admin Site (analytics dashboard) ─────────────────────────────────

class AISolutionsAdminSite(admin.AdminSite):

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('analytics/', self.admin_view(self.analytics_view), name='analytics_dashboard'),
            path('analytics/data/', self.admin_view(self.analytics_data), name='analytics_data'),
        ]
        return custom + urls

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self._get_dashboard_context())
        return super().index(request, extra_context)

    def _get_dashboard_context(self):
        today = timezone.now().date()
        week_ago = today - timedelta(days=6)
        colors_pool = ['#2E86DE', '#22c55e', '#FBB040', '#a855f7', '#ef4444', '#06b6d4', '#f97316', '#ec4899']

        # ── Contact chart (last 7 days) ──────────────────────────────
        contacts_qs = (
            ContactMessage.objects
            .filter(created_at__date__gte=week_ago)
            .annotate(day=TruncDate('created_at'))
            .values('day').annotate(count=Count('id')).order_by('day')
        )
        day_map = {row['day']: row['count'] for row in contacts_qs}
        chart_labels, chart_data = [], []
        for i in range(7):
            d = week_ago + timedelta(days=i)
            chart_labels.append(d.strftime('%b %d'))
            chart_data.append(day_map.get(d, 0))

        # ── Blog by category donut ───────────────────────────────────
        blog_cats = (
            BlogPost.objects.values('category')
            .annotate(count=Count('id')).order_by('-count')
        )
        pie_labels = [r['category'] or 'Uncategorized' for r in blog_cats]
        pie_data   = [r['count'] for r in blog_cats]
        pie_colors = [colors_pool[i % len(colors_pool)] for i in range(len(pie_labels))]

        # ── Service OFFERINGS by category bar ───────────────────────
        offering_cats = (
            Service.objects.filter(record_type=Service.TYPE_SERVICE)
            .values('category').annotate(count=Count('id')).order_by('-count')
        )
        cat_display = dict(Service.CATEGORY_CHOICES)
        svc_offering_labels = [cat_display.get(r['category'], r['category']) for r in offering_cats]
        svc_offering_data   = [r['count'] for r in offering_cats]

        # ── Portfolio projects by category donut ────────────────────
        portfolio_cats = (
            Service.objects.filter(record_type=Service.TYPE_PORTFOLIO)
            .values('category').annotate(count=Count('id')).order_by('-count')
        )
        portfolio_labels = [cat_display.get(r['category'], r['category']) for r in portfolio_cats]
        portfolio_data   = [r['count'] for r in portfolio_cats]
        portfolio_colors = [colors_pool[i % len(colors_pool)] for i in range(len(portfolio_labels))]

        # ── Category comparison table ────────────────────────────────
        all_cats = set(
            list(Service.objects.filter(record_type=Service.TYPE_SERVICE).values_list('category', flat=True)) +
            list(Service.objects.filter(record_type=Service.TYPE_PORTFOLIO).values_list('category', flat=True))
        )
        offering_map  = {r['category']: r['count'] for r in offering_cats}
        portfolio_map = {r['category']: r['count'] for r in portfolio_cats}
        category_comparison = []
        for cat in sorted(all_cats):
            o = offering_map.get(cat, 0)
            p = portfolio_map.get(cat, 0)
            category_comparison.append({
                'label': cat_display.get(cat, cat),
                'offerings': o,
                'portfolio': p,
                'total': o + p,
            })
        category_comparison.sort(key=lambda x: -x['total'])

        # ── Testimonial rating distribution ──────────────────────────
        rating_dist = (
            Testimonial.objects.filter(is_active=True)
            .values('rating').annotate(count=Count('id')).order_by('rating')
        )
        rating_labels = [str(r['rating']) for r in rating_dist]
        rating_data   = [r['count'] for r in rating_dist]

        return {
            # Overall stats
            'dash_stats': {
                'total_contacts':      ContactMessage.objects.count(),
                'unread_contacts':     ContactMessage.objects.filter(is_read=False).count(),
                'total_services':      Service.objects.count(),
                'featured_services':   Service.objects.filter(is_featured=True).count(),
                'total_blog':          BlogPost.objects.count(),
                'published_blog':      BlogPost.objects.filter(is_published=True).count(),
                'total_events':        Event.objects.count(),
                'upcoming_events':     Event.objects.filter(is_completed=False).count(),
                'total_testimonials':  Testimonial.objects.count(),
                'active_testimonials': Testimonial.objects.filter(is_active=True).count(),
                'total_gallery':       GalleryImage.objects.count(),
                'pending_testimonials':Testimonial.objects.filter(is_active=False).count(),
            },
            # Services vs Portfolio counts
            'svc_offering_count':    Service.objects.filter(record_type=Service.TYPE_SERVICE).count(),
            'svc_featured_count':    Service.objects.filter(record_type=Service.TYPE_SERVICE, is_featured=True).count(),
            'portfolio_count':       Service.objects.filter(record_type=Service.TYPE_PORTFOLIO).count(),
            'portfolio_industry_count': len(portfolio_labels),
            # Charts — contact line
            'chart_labels':          json.dumps(chart_labels),
            'chart_data':            json.dumps(chart_data),
            # Charts — blog donut
            'pie_labels':            json.dumps(pie_labels),
            'pie_data':              json.dumps(pie_data),
            'pie_colors':            json.dumps(pie_colors),
            # Charts — service offerings bar
            'svc_offering_labels':   json.dumps(svc_offering_labels),
            'svc_offering_data':     json.dumps(svc_offering_data),
            # Charts — portfolio donut
            'portfolio_labels':      json.dumps(portfolio_labels),
            'portfolio_data':        json.dumps(portfolio_data),
            'portfolio_colors':      json.dumps(portfolio_colors),
            # Charts — rating bar
            'rating_labels':         json.dumps(rating_labels),
            'rating_data':           json.dumps(rating_data),
            # Table
            'category_comparison':   category_comparison,
            # Recent messages
            'recent_contacts':       ContactMessage.objects.order_by('-created_at')[:6],
        }

    def analytics_view(self, request):
        context = dict(self.each_context(request))
        context.update(self._get_dashboard_context())
        context['title'] = 'Analytics Dashboard'
        return render(request, 'admin/analytics_dashboard.html', context)

    def analytics_data(self, request):
        ctx = self._get_dashboard_context()
        return JsonResponse({
            'chart_labels': json.loads(ctx['chart_labels']),
            'chart_data': json.loads(ctx['chart_data']),
            'pie_labels': json.loads(ctx['pie_labels']),
            'pie_data': json.loads(ctx['pie_data']),
        })


# Replace default admin site
admin.site.__class__ = AISolutionsAdminSite
