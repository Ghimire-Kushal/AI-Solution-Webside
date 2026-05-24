import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Service, Testimonial, BlogPost, GalleryImage, Event
from .forms import ContactForm


def home(request):
    services = Service.objects.all()[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:5]
    return render(request, 'core/home.html', {
        'services': services,
        'testimonials': testimonials,
    })


def about(request):
    return render(request, 'core/about.html')


def services(request):
    portfolio = Service.objects.all()
    return render(request, 'core/services.html', {'portfolio': portfolio})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thank you! Your message has been sent. We will get back to you within 24 hours.'
            )
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    gallery = GalleryImage.objects.all()
    return render(request, 'core/blog.html', {'posts': posts, 'gallery': gallery})


def events(request):
    all_events = Event.objects.all()
    upcoming = all_events.filter(is_completed=False)
    completed = all_events.filter(is_completed=True)
    return render(request, 'core/events.html', {
        'upcoming': upcoming,
        'completed': completed,
        'all_events': all_events,
    })


def feedback(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'core/feedback.html', {'testimonials': testimonials})


# ─── Gemini AI Chatbot API ────────────────────────────────────
@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == 'your-gemini-api-key-here':
            # Demo mode — no API key configured
            demo_replies = [
                "Hi! I'm Aria, AI-Solutions' virtual assistant. We offer AI Virtual Assistants, Workflow Automation, Data Analytics, AI Security Monitoring, and Custom AI Development. How can I help you?",
                "Our portfolio includes HealthSync AI (healthcare), RetailMind (retail analytics), EduNova (education), FleetPilot AI (logistics), and SecureVision (security). Which interests you?",
                "To book a free AI consultation, please visit our Contact page or email us at hello@ai-solutions.com. Our team will respond within 24 hours.",
                "AI-Solutions is based in Kathmandu, Nepal, serving 500+ companies worldwide. We specialize in making AI practical and affordable for real businesses.",
                "Great question! Our implementations typically go live in 2–4 weeks. We handle everything from setup to training. Would you like to schedule a demo?",
            ]
            import hashlib
            idx = int(hashlib.md5(user_message.encode()).hexdigest(), 16) % len(demo_replies)
            return JsonResponse({'response': demo_replies[idx], 'mode': 'demo'})

        from google import genai as google_genai

        client = google_genai.Client(api_key=settings.GEMINI_API_KEY)

        system_context = (
            "You are Aria, the professional AI virtual assistant for AI-Solutions — "
            "a tech startup based in Kathmandu, Nepal, specializing in AI-powered workplace automation. "
            "Company info: Services include AI Virtual Assistants, Workflow Automation, Data Analytics, "
            "AI Security Monitoring, AI Consultation, and Custom AI Development. "
            "Portfolio: HealthSync AI (healthcare), RetailMind (retail), EduNova (education), "
            "FleetPilot AI (logistics), SecureVision (security). "
            "Contact: hello@ai-solutions.com | +977 98XXXXXXXX | Tagline: Innovate | Support | Empower. "
            "Rules: Be professional, helpful, and concise. Focus on AI-Solutions services. "
            "For pricing, direct users to book a free consultation. "
            "Keep responses under 3 sentences unless detail is truly needed. "
            f"User message: {user_message}"
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=system_context,
        )
        return JsonResponse({'response': response.text, 'mode': 'live'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        error_str = str(e)
        # Rate limit — give a friendly message instead of an error
        if '429' in error_str or 'RESOURCE_EXHAUSTED' in error_str or 'quota' in error_str.lower():
            return JsonResponse({
                'response': (
                    "I'm receiving a lot of questions right now! 😊 "
                    "Please wait a moment and try again, or contact us directly at "
                    "hello@ai-solutions.com for immediate assistance."
                )
            })
        return JsonResponse({
            'response': (
                'I apologize — I encountered a technical issue. '
                'Please try again or email us at hello@ai-solutions.com.'
            )
        })
