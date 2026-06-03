import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

CATEGORY_IMAGES = [
    ('healthcare', 'Healthcare',          'images/service-healthcare.svg'),
    ('retail',     'Retail & Commerce',   'images/service-retail.svg'),
    ('education',  'Education',           'images/service-education.svg'),
    ('logistics',  'Logistics & Transport','images/service-logistics.svg'),
    ('security',   'Security',            'images/service-security.svg'),
    ('other',      'Custom / Other',      'images/service-other.svg'),
]

from django.db.models import Count
from core.models import Service, ServiceOffering, Testimonial, BlogPost, GalleryImage, Event, ContactMessage, SiteSettings
from .forms import (ServiceForm, ServiceOfferingForm, TestimonialForm, BlogPostForm,
                    GalleryImageForm, EventForm, SiteSettingsForm, CustomPasswordChangeForm)


def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('panel_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('panel_dashboard')
        messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'panel/login.html')


def panel_logout_view(request):
    logout(request)
    return redirect('panel_login')


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('panel_login')
        if not request.user.is_staff:
            messages.error(request, 'Access denied.')
            return redirect('panel_login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── Dashboard ────────────────────────────────────────────────
@staff_required
def dashboard(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    stats = {
        'total_contacts': ContactMessage.objects.count(),
        'unread_contacts': ContactMessage.objects.filter(is_read=False).count(),
        'total_services': Service.objects.count(),
        'total_blog': BlogPost.objects.count(),
        'published_blog': BlogPost.objects.filter(is_published=True).count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(is_completed=False).count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_gallery': GalleryImage.objects.count(),
    }

    recent_contacts = ContactMessage.objects.all()[:5]

    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        count = ContactMessage.objects.filter(created_at__date=day.date()).count()
        chart_labels.append(day.strftime('%b %d'))
        chart_data.append(count)

    # Blog posts by category for donut chart
    cat_qs = (
        BlogPost.objects
        .values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    pie_labels = [c['category'] or 'Uncategorised' for c in cat_qs]
    pie_data   = [c['count'] for c in cat_qs]
    pie_colors = [
        '#2E86DE','#a855f7','#22c55e','#f97316',
        '#ef4444','#22d3ee','#FBB040','#64748b',
    ][:len(pie_labels)]

    return render(request, 'panel/dashboard.html', {
        'stats': stats,
        'recent_contacts': recent_contacts,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
        'pie_colors': pie_colors,
    })


# ─── Service Offerings ────────────────────────────────────────
@staff_required
def service_offerings_list(request):
    return render(request, 'panel/service_offerings_list.html', {
        'offerings': ServiceOffering.objects.all()
    })


@staff_required
def service_offering_add(request):
    form = ServiceOfferingForm(request.POST or None, request.FILES or None)
    features_json = '["Feature 1","Feature 2","Feature 3"]'
    if request.method == 'POST':
        features_json = request.POST.get('features', features_json)
        if form.is_valid():
            obj = form.save(commit=False)
            try:
                obj.features = json.loads(request.POST.get('features', '[]'))
            except (json.JSONDecodeError, ValueError):
                obj.features = []
            obj.save()
            messages.success(request, 'Service offering added.')
            return redirect('panel_service_offerings')
    return render(request, 'panel/service_offering_form.html', {
        'form': form, 'action': 'Add', 'features_json': features_json,
    })


@staff_required
def service_offering_edit(request, pk):
    obj = get_object_or_404(ServiceOffering, pk=pk)
    form = ServiceOfferingForm(request.POST or None, request.FILES or None, instance=obj)
    features_json = json.dumps(obj.features) if obj.features else '[]'
    if request.method == 'POST':
        features_json = request.POST.get('features', features_json)
        if form.is_valid():
            svc = form.save(commit=False)
            try:
                svc.features = json.loads(request.POST.get('features', '[]'))
            except (json.JSONDecodeError, ValueError):
                svc.features = []
            svc.save()
            messages.success(request, 'Service offering updated.')
            return redirect('panel_service_offerings')
    return render(request, 'panel/service_offering_form.html', {
        'form': form, 'action': 'Edit', 'obj': obj, 'features_json': features_json,
    })


@staff_required
def service_offering_delete(request, pk):
    obj = get_object_or_404(ServiceOffering, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Service offering deleted.')
    return redirect('panel_service_offerings')


# ─── Services / Portfolio ──────────────────────────────────────
@staff_required
def services_list(request):
    return render(request, 'panel/services_list.html', {'services': Service.objects.all()})


@staff_required
def service_add(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    features_json = '["Feature 1","Feature 2","Feature 3"]'
    if request.method == 'POST':
        features_json = request.POST.get('features', features_json)
        if form.is_valid():
            obj = form.save(commit=False)
            try:
                obj.features = json.loads(request.POST.get('features', '[]'))
            except (json.JSONDecodeError, ValueError):
                obj.features = []
            obj.save()
            messages.success(request, 'Service added successfully.')
            return redirect('panel_services')
    return render(request, 'panel/service_form.html', {
        'form': form, 'action': 'Add',
        'features_json': features_json,
        'category_images': CATEGORY_IMAGES,
    })


@staff_required
def service_edit(request, pk):
    obj = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=obj)
    features_json = json.dumps(obj.features) if obj.features else '[]'
    if request.method == 'POST':
        features_json = request.POST.get('features', features_json)
        if form.is_valid():
            svc = form.save(commit=False)
            try:
                svc.features = json.loads(request.POST.get('features', '[]'))
            except (json.JSONDecodeError, ValueError):
                svc.features = []
            svc.save()
            messages.success(request, 'Service updated.')
            return redirect('panel_services')
    return render(request, 'panel/service_form.html', {
        'form': form, 'action': 'Edit', 'obj': obj,
        'features_json': features_json,
        'category_images': CATEGORY_IMAGES,
    })


@staff_required
def service_delete(request, pk):
    obj = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Service deleted.')
    return redirect('panel_services')


# ─── Blog ─────────────────────────────────────────────────────
@staff_required
def blog_list(request):
    return render(request, 'panel/blog_list.html', {'posts': BlogPost.objects.all()})


@staff_required
def blog_add(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Blog post added.')
        return redirect('panel_blog')
    return render(request, 'panel/blog_form.html', {'form': form, 'action': 'Add'})


@staff_required
def blog_edit(request, pk):
    obj = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Blog post updated.')
        return redirect('panel_blog')
    return render(request, 'panel/blog_form.html', {'form': form, 'action': 'Edit', 'obj': obj})


@staff_required
def blog_delete(request, pk):
    obj = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Post deleted.')
    return redirect('panel_blog')


# ─── Gallery ──────────────────────────────────────────────────
@staff_required
def gallery_list(request):
    form = GalleryImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Image uploaded.')
        return redirect('panel_gallery')
    return render(request, 'panel/gallery_list.html', {
        'images': GalleryImage.objects.all(), 'form': form
    })


@staff_required
def gallery_delete(request, pk):
    obj = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        obj.image.delete(save=False)
        obj.delete()
        messages.success(request, 'Image deleted.')
    return redirect('panel_gallery')


# ─── Events ───────────────────────────────────────────────────
@staff_required
def events_list(request):
    return render(request, 'panel/events_list.html', {'events': Event.objects.all()})


@staff_required
def event_add(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Event added.')
        return redirect('panel_events')
    return render(request, 'panel/event_form.html', {'form': form, 'action': 'Add'})


@staff_required
def event_edit(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Event updated.')
        return redirect('panel_events')
    return render(request, 'panel/event_form.html', {'form': form, 'action': 'Edit', 'obj': obj})


@staff_required
def event_delete(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Event deleted.')
    return redirect('panel_events')


# ─── Contact Messages ─────────────────────────────────────────
@staff_required
def contacts_list(request):
    return render(request, 'panel/contacts_list.html', {'contacts': ContactMessage.objects.all()})


@staff_required
def contact_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, 'panel/contact_detail.html', {'msg': msg})


@staff_required
def contact_delete(request, pk):
    obj = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Message deleted.')
    return redirect('panel_contacts')


# ─── Testimonials ─────────────────────────────────────────────
@staff_required
def testimonials_list(request):
    return render(request, 'panel/testimonials_list.html', {'testimonials': Testimonial.objects.all()})


@staff_required
def testimonial_add(request):
    form = TestimonialForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Testimonial added.')
        return redirect('panel_testimonials')
    return render(request, 'panel/testimonial_form.html', {'form': form, 'action': 'Add'})


@staff_required
def testimonial_edit(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk)
    form = TestimonialForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Testimonial updated.')
        return redirect('panel_testimonials')
    return render(request, 'panel/testimonial_form.html', {'form': form, 'action': 'Edit', 'obj': obj})


@staff_required
def testimonial_delete(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Testimonial deleted.')
    return redirect('panel_testimonials')


# ─── Site Settings ────────────────────────────────────────────
@staff_required
def site_settings_view(request):
    obj = SiteSettings.get_settings()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Site settings updated.')
        return redirect('panel_settings')
    return render(request, 'panel/settings.html', {'form': form})


# ─── Password Change ──────────────────────────────────────────
@staff_required
def change_password(request):
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password updated successfully.')
        return redirect('panel_dashboard')
    return render(request, 'panel/password.html', {'form': form})
