import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

<<<<<<< HEAD
from .models import Service, ServiceOffering, Testimonial, BlogPost, GalleryImage, Event
from .forms import ContactForm
=======
from django.shortcuts import get_object_or_404
from .models import Service, Testimonial, BlogPost, GalleryImage, Event
from .forms import ContactForm, TestimonialSubmitForm
>>>>>>> e63a2c1 (fix bug)


def home(request):
    # Show service offerings (no client_name) — have real images
    services = Service.objects.filter(record_type='service', is_featured=True).order_by('order')[:6]
    if services.count() < 3:
        services = Service.objects.filter(record_type='service').order_by('order')[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    return render(request, 'core/home.html', {
        'services': services,
        'testimonials': testimonials,
    })


def about(request):
    team_members = [
        {'name': 'Pratik Rauniyar', 'initials': 'PR', 'role': 'Founder & Lead Developer', 'bio': 'Full-stack AI engineer with a focus on practical NLP and automation solutions.'},
        {'name': 'Rishav Chudal', 'initials': 'RC', 'role': 'Client & Project Lead', 'bio': 'Bridges the gap between client requirements and technical delivery on every engagement.'},
        {'name': 'QA Specialist', 'initials': 'QA', 'role': 'Quality Assurance', 'bio': 'Ensures every deployment is bulletproof — from unit tests to full production stress testing.'},
        {'name': 'Expert Advisor', 'initials': 'EA', 'role': 'Technical Advisor', 'bio': 'Senior ML advisor guiding architecture decisions and model selection for complex builds.'},
    ]
    tech_stack = [
        {'name': 'Python', 'icon': 'bi bi-code-slash'},
        {'name': 'Django', 'icon': 'bi bi-server'},
        {'name': 'TensorFlow', 'icon': 'bi bi-cpu'},
        {'name': 'PyTorch', 'icon': 'bi bi-lightning-charge'},
        {'name': 'Google Gemini', 'icon': 'bi bi-stars'},
        {'name': 'OpenAI API', 'icon': 'bi bi-robot'},
        {'name': 'PostgreSQL', 'icon': 'bi bi-database'},
        {'name': 'Docker', 'icon': 'bi bi-box'},
        {'name': 'AWS / GCP', 'icon': 'bi bi-cloud'},
        {'name': 'React', 'icon': 'bi bi-braces'},
        {'name': 'REST APIs', 'icon': 'bi bi-arrow-left-right'},
        {'name': 'Computer Vision', 'icon': 'bi bi-eye'},
    ]
    return render(request, 'core/about.html', {
        'team_members': team_members,
        'tech_stack': tech_stack,
    })


def services_page(request):
    offerings = ServiceOffering.objects.filter(is_active=True)
    process_steps = [
        {'icon': 'bi-search', 'title': 'Discovery', 'desc': 'We audit your processes and identify the highest-impact AI opportunities.'},
        {'icon': 'bi-layout-text-window', 'title': 'Design', 'desc': 'A tailored solution blueprint with timelines, integrations, and ROI projections.'},
        {'icon': 'bi-code-slash', 'title': 'Build & Train', 'desc': 'Rapid development, model training, and testing with your real data.'},
        {'icon': 'bi-rocket-takeoff', 'title': 'Deploy & Support', 'desc': 'Live deployment plus ongoing monitoring, updates, and dedicated support.'},
    ]
    return render(request, 'core/services_page.html', {'offerings': offerings, 'process_steps': process_steps})


def services(request):
    offerings = Service.objects.filter(record_type='service').order_by('order')
    steps = [
        {'title': 'Discovery & Scoping', 'desc': 'We learn your business, data landscape, and goals in a free consultation session.'},
        {'title': 'Design & Prototype', 'desc': 'Our team designs the solution architecture and delivers a working prototype for feedback.'},
        {'title': 'Build & Integrate', 'desc': 'Full development, QA testing, and integration with your existing systems and workflows.'},
        {'title': 'Deploy & Support', 'desc': 'Live deployment with full documentation, team training, and ongoing monitoring support.'},
    ]
    why_stats = [
        {'value': '50+', 'label': 'Projects Delivered'},
        {'value': '98%', 'label': 'Client Satisfaction'},
        {'value': '6+', 'label': 'Industries Served'},
        {'value': '24/7', 'label': 'Post-Launch Support'},
    ]
    return render(request, 'core/services.html', {
        'portfolio': offerings,
        'steps': steps,
        'why_stats': why_stats,
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related = Service.objects.filter(category=service.category).exclude(pk=service.pk)[:3]
    return render(request, 'core/service_detail.html', {'service': service, 'related': related})


def portfolio(request):
    category = request.GET.get('category', '')
    qs = Service.objects.filter(record_type='portfolio').order_by('order')
    if category:
        qs = qs.filter(category=category)
    categories = Service.CATEGORY_CHOICES
    return render(request, 'core/portfolio.html', {
        'projects': qs,
        'categories': categories,
        'active_category': category,
    })


def portfolio_detail(request, slug):
    project = get_object_or_404(Service, slug=slug)
    related = Service.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
    testimonials = Testimonial.objects.filter(
        project_name__icontains=project.title, is_active=True
    )[:3]
    return render(request, 'core/portfolio_detail.html', {
        'project': project,
        'related': related,
        'testimonials': testimonials,
    })


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
    return render(request, 'core/blog.html', {'posts': posts})


def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'core/gallery.html', {'images': images})


def blog_detail(request, slug):
    from django.shortcuts import get_object_or_404
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    return render(request, 'core/blog_detail.html', {'post': post, 'recent': recent})


def events(request):
    tab = request.GET.get('tab', 'upcoming')
    upcoming  = Event.objects.filter(is_completed=False).order_by('date')
    past      = Event.objects.filter(is_completed=True).order_by('-date')
    return render(request, 'core/events.html', {
        'upcoming': upcoming,
        'past': past,
        'active_tab': tab,
    })


def event_detail(request, pk):
    from django.shortcuts import get_object_or_404
    event = get_object_or_404(Event, pk=pk)
    related = Event.objects.exclude(pk=pk).order_by('-date')[:3]
    return render(request, 'core/event_detail.html', {
        'event': event,
        'related': related,
    })


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def cookie_policy(request):
    return render(request, 'core/cookie_policy.html')


def feedback(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    form = TestimonialSubmitForm()
    if request.method == 'POST':
        form = TestimonialSubmitForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.is_active = False  # pending admin approval
            t.save()
            messages.success(request, 'Thank you for your review! It will appear after approval.')
            return redirect('feedback')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'core/feedback.html', {'testimonials': testimonials, 'form': form})


# ─── Aria Chatbot — OpenRouter ────────────────────────────────

ARIA_SYSTEM_PROMPT = """You are Aria, the intelligent virtual assistant for AI-Solutions — a technology company based in Kathmandu, Nepal, with an upcoming UK office in Sunderland. You are embedded on the AI-Solutions website and your job is to help visitors learn about the company, its services, portfolio, and how to get started.

=== COMPANY OVERVIEW ===
Name: AI-Solutions
Tagline: Innovate | Support | Empower
Founded: 2024, Kathmandu, Nepal
Mission: Making AI practical, affordable, and impactful for real businesses.
Upcoming expansion: UK Office opening in Sunderland, 2026.
Email: student.helpline@sunderland.ac.uk
Phone: +44 191 515 3000
Address: Chester Road, Sunderland, UK, SR1 3SD
Hours: Sunday–Friday, 9:00 AM – 6:00 PM (NPT)

=== TEAM ===
- Pratik Rauniyar — Founder & Lead Developer. Full-stack AI engineer focused on NLP and automation.
- Rishav Chudal — Client & Project Lead. Bridges client requirements and technical delivery.
- QA Specialist — Ensures every deployment is bulletproof from unit tests to production.
- Expert Advisor — Senior ML advisor guiding architecture and model selection.

=== SERVICES ===
1. AI Virtual Assistants — Custom AI chatbots and voice assistants for customer support, internal helpdesks, and front-desk automation. Available 24/7. Integrates with CRM, ticketing, and email systems.
2. Workflow Automation — Automate repetitive business processes using AI. Document processing, approval workflows, data entry, scheduling.
3. Data Analytics & Intelligence — Turn raw business data into actionable insights. Dashboards, forecasting models, customer behavior analysis.
4. AI Security Monitoring — Real-time threat detection, fraud prevention, and anomaly detection powered by AI.
5. AI Consultation — Free initial consultation to identify your best AI starting point. We assess your processes, data, and goals.
6. Custom AI Development — Bespoke AI solutions built from scratch for unique business problems. Full-cycle: discovery, design, build, deploy, support.

=== PORTFOLIO (Past Projects) ===
1. HealthSync AI (Client: Horizon Care | Sector: Healthcare)
   - AI-powered healthcare workflow and patient management platform
   - Features: Automated appointment scheduling, Predictive patient risk alerts, Real-time record synchronization, AI-assisted diagnostics, Wearable device integration
   - Result: Reduced patient waiting times by 35%, flagged critical risk cases in real time

2. RetailMind (Client: UrbanStyle | Sector: Retail & Commerce)
   - Retail analytics and customer behavior intelligence solution
   - Features: Customer movement tracking, Sales forecasting, Inventory optimization, Product placement recommendations, POS and CRM integration
   - Result: 25% reduction in overstock costs within first month

3. EduNova (Client: Nova International College | Sector: Education)
   - AI-based adaptive learning and education management system
   - Features: Personalized learning modules, Automated grading, AI-generated quizzes, Student engagement analytics, Multilingual support
   - Result: 40% improvement in student engagement, module completion rate jumped from 54% to 89%

4. FleetPilot AI (Client: SwiftMove Logistics | Sector: Logistics & Transport)
   - Transportation and logistics optimization platform
   - Features: Live vehicle tracking, Route optimization, Fuel prediction analytics, Driver performance insights, Delivery scheduling automation
   - Result: 30% reduction in delivery times within two months

5. SecureVision (Client: Nexa Corporate Solutions | Sector: Security)
   - AI-driven surveillance and security monitoring solution
   - Features: Real-time threat detection, Facial recognition access control, Suspicious activity alerts, Cloud-based security analytics, Remote monitoring dashboard
   - Result: Fully replaced legacy access card system with AI-powered access control

=== TESTIMONIALS ===
- Dr. Melissa Carter (Horizon Care): "HealthSync AI improved our hospital operations significantly and reduced patient waiting times." — 4.8/5
- Daniel Brooks (UrbanStyle): "RetailMind helped us understand customer behavior better and increase overall revenue." — 4.7/5
- Priya Sharma (Nova International College): "EduNova transformed the learning experience for our students with personalized AI recommendations." — 4.9/5
- Eric Thompson (SwiftMove Logistics): "FleetPilot AI streamlined our delivery network and improved fuel efficiency." — 4.6/5
- Karen White (Nexa Corporate Solutions): "SecureVision strengthened our security infrastructure with real-time monitoring and alerts." — 4.8/5

=== KEY STATS ===
- 50+ Projects Delivered
- 98% Client Satisfaction
- 6+ Industries Served
- 24/7 Post-Launch Support
- Typical implementation: 2–4 weeks from agreement to go-live

=== HOW TO GET STARTED ===
- Visit /contact to send a message or book a free consultation
- Email: student.helpline@sunderland.ac.uk
- The team responds within 24 hours

=== SCENARIO HANDLING RULES ===
- Pricing questions: Never give specific prices. Direct to book a free consultation at /contact or email student.helpline@sunderland.ac.uk.
- Technical questions: Answer clearly based on the portfolio and services above. If unsure, recommend contacting the team.
- Competitor comparisons: Stay neutral and professional. Focus on AI-Solutions' strengths.
- Off-topic questions (politics, general knowledge, personal advice): Politely steer back — "I'm here to help with anything AI-Solutions related. What can I help you with?"
- Negative feedback or complaints: Acknowledge, empathize, and direct to student.helpline@sunderland.ac.uk for resolution.
- Greetings: Respond warmly and ask how you can help.
- If someone wants to apply for a job: Direct them to email student.helpline@sunderland.ac.uk with their CV and the role they're interested in.

=== TONE & STYLE ===
- Professional but friendly and approachable
- Concise — 2 to 4 sentences per response unless the question genuinely needs more detail
- Use bullet points for feature lists or multi-part answers
- Never make up facts not listed above
- Sign off occasionally with: "Is there anything else I can help you with?"
"""


@require_POST
def chat_api(request):
    import requests as http_requests

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        history = data.get('history', [])  # list of {role, content} dicts from frontend

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        api_key = getattr(settings, 'OPENROUTER_API_KEY', '')

        if not api_key:
            return JsonResponse({
                'response': (
                    "Hi! I'm Aria, AI-Solutions' virtual assistant. "
                    "Our services include AI Virtual Assistants, Workflow Automation, Data Analytics, "
                    "AI Security Monitoring, and Custom AI Development. "
                    "Visit our Contact page or email student.helpline@sunderland.ac.uk to get started!"
                ),
                'mode': 'demo'
            })

        # Build message list: system prompt + conversation history + new user message
        messages = [{'role': 'system', 'content': ARIA_SYSTEM_PROMPT}]

        # Include up to last 10 exchanges for context
        for turn in history[-10:]:
            role = turn.get('role', '')
            content = turn.get('content', '')
            if role in ('user', 'assistant') and content:
                messages.append({'role': role, 'content': content})

        messages.append({'role': 'user', 'content': user_message})

        response = http_requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://ai-solutions.com',
                'X-Title': 'AI-Solutions Aria Chatbot',
            },
            json={
                'model': 'meta-llama/llama-3.3-70b-instruct',
                'messages': messages,
                'max_tokens': 500,
                'temperature': 0.7,
            },
            timeout=20,
        )

        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content'].strip()
            return JsonResponse({'response': reply, 'mode': 'live'})

        # Handle rate limit or server errors gracefully
        if response.status_code == 429:
            return JsonResponse({
                'response': (
                    "I'm handling a lot of conversations right now! "
                    "Please try again in a moment, or reach us directly at student.helpline@sunderland.ac.uk."
                )
            })

        return JsonResponse({
            'response': (
                "I encountered a technical issue. Please try again or "
                "email us at student.helpline@sunderland.ac.uk — we'll get back to you within 24 hours."
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception:
        return JsonResponse({
            'response': (
                "I'm having trouble connecting right now. Please email us at "
                "student.helpline@sunderland.ac.uk and we'll respond within 24 hours."
            )
        })
