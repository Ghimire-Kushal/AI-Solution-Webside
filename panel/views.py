from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from core.models import Service, Testimonial, BlogPost, GalleryImage, Event, ContactMessage, SiteSettings
from .forms import (ServiceForm, TestimonialForm, BlogPostForm,
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

    return render(request, 'panel/dashboard.html', {
        'stats': stats,
        'recent_contacts': recent_contacts,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })


# ─── Services ─────────────────────────────────────────────────
@staff_required
def services_list(request):
    return render(request, 'panel/services_list.html', {'services': Service.objects.all()})


@staff_required
def service_add(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Service added successfully.')
        return redirect('panel_services')
    return render(request, 'panel/service_form.html', {'form': form, 'action': 'Add'})


@staff_required
def service_edit(request, pk):
    obj = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Service updated.')
        return redirect('panel_services')
    return render(request, 'panel/service_form.html', {'form': form, 'action': 'Edit', 'obj': obj})


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
